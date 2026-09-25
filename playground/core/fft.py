"""Discrete Fourier transform built from scratch (Ashraf Sir, Lectures 1-4).

* Radix-2 decimation-in-time FFT: bit-reverse the input, then log2 N butterfly
  stages  X[k] = G[k] + W_N^k H[k],  X[k + N/2] = G[k] - W_N^k H[k].
  Every stage is vectorised over all the rows at once.
* General Cooley–Tukey N = N1·N2 for composite lengths: rows DFT, twiddle,
  columns DFT (Bailey's four-step view), recursing until a power of 2 remains.
* Bluestein (chirp-z) for large prime lengths: kn = (k^2 + n^2 - (k - n)^2) / 2
  turns the DFT into a linear convolution with a chirp, which is run as a
  zero-padded radix-2 fast convolution.
* The inverse uses conjugation: IDFT{X} = conj(DFT{conj(X)}) / N.
* 2D transforms are row DFTs followed by column DFTs (the tabular / Bailey view).
* Fast convolution: zero-pad to at least L + M - 1 so that the circular
  convolution computed by multiplying DFTs equals the linear one.
"""

from __future__ import annotations

from functools import lru_cache

import numpy as np


def next_pow2(n: int) -> int:
    return 1 if n <= 1 else 1 << (int(n) - 1).bit_length()


def is_pow2(n: int) -> bool:
    return n >= 1 and n & (n - 1) == 0


def good_size(n: int) -> int:
    """Smallest length >= n whose only prime factors are 2, 3 and 5 (fast Cooley–Tukey)."""
    best = next_pow2(n)
    p5 = 1
    while p5 < best:
        p35 = p5
        while p35 < best:
            m = p35
            while m < n:
                m *= 2
            best = min(best, m)
            p35 *= 3
        p5 *= 5
    return best


@lru_cache(maxsize=None)
def bit_reversed_indices(n: int) -> np.ndarray:
    """Input order of an n-point DIT FFT, e.g. n = 8 -> [0, 4, 2, 6, 1, 5, 3, 7]."""
    bits = n.bit_length() - 1
    idx = np.arange(n)
    rev = np.zeros(n, dtype=np.int64)
    for b in range(bits):
        rev |= ((idx >> b) & 1) << (bits - 1 - b)
    return rev


@lru_cache(maxsize=None)
def _twiddles(size: int) -> np.ndarray:
    """W_size^k for k = 0 .. size/2 - 1."""
    return np.exp(-2j * np.pi * np.arange(size // 2) / size)


def _fft_radix2(x: np.ndarray) -> np.ndarray:
    """Iterative radix-2 DIT FFT along the last axis (length must be a power of 2)."""
    n = x.shape[-1]
    lead = x.shape[:-1]
    x = x[..., bit_reversed_indices(n)]
    size = 2
    while size <= n:
        half = size // 2
        blocks = x.reshape(*lead, n // size, size)
        g = blocks[..., :half]                      # DFTs of the even-indexed half
        h = blocks[..., half:] * _twiddles(size)    # twiddled DFTs of the odd half
        x = np.concatenate((g + h, g - h), axis=-1).reshape(*lead, n)
        size *= 2
    return x


@lru_cache(maxsize=None)
def _bluestein_chirps(n: int) -> tuple[np.ndarray, np.ndarray, int]:
    m = next_pow2(2 * n - 1)
    k = np.arange(n)
    # W_{2N}^{k^2}; k^2 is reduced mod 2N (the chirp's period) to keep precision
    chirp = np.exp(-1j * np.pi * ((k * k) % (2 * n)) / n)
    b = np.zeros(m, dtype=complex)
    b[:n] = np.conj(chirp)                 # b[n] = W_{2N}^{-n^2}, n >= 0
    b[m - n + 1:] = np.conj(chirp[1:])[::-1]  # negative n wrapped to the end of the buffer
    return chirp, _fft_radix2(b), m


def _fft_bluestein(x: np.ndarray) -> np.ndarray:
    n = x.shape[-1]
    chirp, b_spec, m = _bluestein_chirps(n)
    a = np.zeros(x.shape[:-1] + (m,), dtype=complex)
    a[..., :n] = x * chirp
    conv = _ifft_any(_fft_radix2(a) * b_spec)
    return conv[..., :n] * chirp


def _smallest_odd_prime_factor(n: int) -> int:
    while n % 2 == 0:
        n //= 2
    p = 3
    while p * p <= n:
        if n % p == 0:
            return p
        p += 2
    return n


@lru_cache(maxsize=None)
def _dft_matrix(n: int) -> np.ndarray:
    k = np.arange(n)
    return np.exp(-2j * np.pi * np.outer(k, k) / n)


@lru_cache(maxsize=None)
def _ct_twiddles(n1: int, n2: int) -> np.ndarray:
    """W_N^{n1 k2} for the N1 × N2 intermediate matrix."""
    return np.exp(-2j * np.pi * np.outer(np.arange(n1), np.arange(n2)) / (n1 * n2))


def _fft_cooley_tukey(x: np.ndarray, n1: int) -> np.ndarray:
    """General Cooley–Tukey N = N1·N2 (Bailey's four steps).

    1. load x column-major into an N1 × N2 matrix: entry (n1, n2) = x[N1 n2 + n1]
    2. N2-point DFT of every row (recursively)
    3. multiply entry (n1, k2) by W_N^{n1 k2}
    4. N1-point DFT down every column; read the result row-major: k = N2 k1 + k2
    """
    n = x.shape[-1]
    n2 = n // n1
    lead = x.shape[:-1]
    rows = np.swapaxes(x.reshape(*lead, n2, n1), -1, -2)       # (..., n1, n2)
    rows = _fft_any(np.ascontiguousarray(rows)) * _ct_twiddles(n1, n2)
    if n1 <= 16:
        cols = np.einsum("kn,...nm->...km", _dft_matrix(n1), rows)
    else:
        cols = np.swapaxes(_fft_bluestein(np.swapaxes(rows, -1, -2)), -1, -2)
    return cols.reshape(*lead, n)


def _fft_any(x: np.ndarray) -> np.ndarray:
    n = x.shape[-1]
    if n == 1:
        return x.copy()
    if is_pow2(n):
        return _fft_radix2(x)
    p = _smallest_odd_prime_factor(n)
    if p == n:                       # prime length: no factorisation helps
        return x @ _dft_matrix(n) if n <= 16 else _fft_bluestein(x)
    return _fft_cooley_tukey(x, p)   # peel one odd prime; the rest recurses


def _ifft_any(x: np.ndarray) -> np.ndarray:
    return np.conj(_fft_any(np.conj(x))) / x.shape[-1]


def fft(x, axis: int = -1) -> np.ndarray:
    """N-point DFT  X[k] = sum_n x[n] W_N^{kn}  along ``axis``."""
    x = np.moveaxis(np.asarray(x, dtype=complex), axis, -1)
    return np.moveaxis(_fft_any(x), -1, axis)


def ifft(x, axis: int = -1) -> np.ndarray:
    """Inverse DFT  x[n] = (1/N) sum_k X[k] W_N^{-kn}  along ``axis``."""
    x = np.moveaxis(np.asarray(x, dtype=complex), axis, -1)
    return np.moveaxis(_ifft_any(x), -1, axis)


def fft2(x) -> np.ndarray:
    """2D DFT over the last two axes: DFT every row, then every column."""
    return fft(fft(x, axis=-1), axis=-2)


def ifft2(x) -> np.ndarray:
    return ifft(ifft(x, axis=-1), axis=-2)


def fftshift(x: np.ndarray) -> np.ndarray:
    """Move bin 0 to the centre (negative frequencies on the left / top)."""
    return np.roll(x, (x.shape[-2] // 2, x.shape[-1] // 2), axis=(-2, -1))


def ifftshift(x: np.ndarray) -> np.ndarray:
    return np.roll(x, (-(x.shape[-2] // 2), -(x.shape[-1] // 2)), axis=(-2, -1))


def freq_grid(shape: tuple[int, int]) -> tuple[np.ndarray, np.ndarray]:
    """Signed bin indices (k for k <= N/2, k - N above) for every 2D bin."""
    def signed(n: int) -> np.ndarray:
        k = np.arange(n)
        return np.where(k <= n // 2, k, k - n)
    return np.meshgrid(signed(shape[0]), signed(shape[1]), indexing="ij")


def log_spectrum(img: np.ndarray) -> np.ndarray:
    """log(1 + |X|), centred — the usual way to look at an image's spectrum."""
    return np.log1p(np.abs(fftshift(fft2(img))))


def kernel_otf(kernel: np.ndarray, shape: tuple[int, int]) -> np.ndarray:
    """DFT of a kernel zero-padded to ``shape`` with its centre moved to (0, 0).

    Multiplying by this spectrum is circular convolution with the kernel centred
    on each pixel (same as ``convolve2d(..., padding='circular')``).
    """
    kh, kw = kernel.shape
    if kh > shape[0] or kw > shape[1]:
        raise ValueError("kernel is larger than the image")
    padded = np.zeros(shape)
    padded[:kh, :kw] = kernel
    return fft2(np.roll(padded, (-(kh // 2), -(kw // 2)), axis=(0, 1)))


def fast_convolve2d(x, h, mode: str = "full") -> np.ndarray:
    """Linear 2D convolution x ⊛ h computed as IDFT{X · H}.

    Both are zero-padded to N >= L + M - 1 per axis, so the circular convolution
    produced by multiplying DFTs equals the linear one. N is chosen with only
    the prime factors 2, 3, 5 so the Cooley–Tukey FFT stays fast.
    mode: 'full' (L + M - 1), 'same' (matches ``convolve2d`` with zero padding),
    'valid' (only positions where h fits entirely inside x), or 'circular'
    (no padding: the wrap is kept, kernel centred).

    A complex x = x1 + j·x2 with a real h convolves two real images for the
    price of one (linearity): the real part is x1 ⊛ h, the imaginary part x2 ⊛ h.
    """
    x = np.asarray(x)
    h = np.asarray(h, dtype=float)
    take = (lambda a: a) if np.iscomplexobj(x) else np.real
    if mode == "circular":
        return take(ifft2(fft2(x) * kernel_otf(h, x.shape)))
    (xh, xw), (kh, kw) = x.shape, h.shape
    fh, fw = xh + kh - 1, xw + kw - 1
    nh, nw = good_size(fh), good_size(fw)
    xp = np.zeros((nh, nw), dtype=complex if np.iscomplexobj(x) else float)
    xp[:xh, :xw] = x
    hp = np.zeros((nh, nw))
    hp[:kh, :kw] = h
    full = take(ifft2(fft2(xp) * fft2(hp)))[:fh, :fw]
    if mode == "full":
        return full
    if mode == "same":
        top, left = kh // 2, kw // 2   # = bottom/right padding of the 'same' scheme
        return full[top:top + xh, left:left + xw]
    if mode == "valid":
        if kh > xh or kw > xw:
            raise ValueError("kernel is larger than the input")
        return full[kh - 1:xh, kw - 1:xw]
    raise ValueError(f"unknown mode {mode!r}")


def fast_correlate2d(x, t, mode: str = "valid") -> np.ndarray:
    """Cross-correlation  r[m, n] = sum x[m + i, n + j] t[i, j]: convolution with t flipped."""
    t = np.asarray(t, dtype=float)
    return fast_convolve2d(x, t[::-1, ::-1], mode)
