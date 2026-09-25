"""Super resolution as sampling-theory reconstruction (Ashraf Sir, Lecture 5).

Upscaling by f means reconstructing the underlying band-limited image from its
samples and re-sampling it on a grid f times finer. Every method is
"insert f - 1 zeros between samples, then low-pass filter":

* zero-order hold      h0 = rect of width f        -> blocky, H0 ~ sinc (leaky)
* linear interpolation h1 = h0 ⊛ h0 (triangle)     -> H1 ~ sinc², less leakage
* ideal (sinc)         brick-wall LPF, cutoff π/f  -> done exactly in the DFT
  domain: zero-pad the spectrum (fill new high bins with 0)

Downsampling without first removing frequencies above the new Nyquist limit
aliases them; ``antialias=True`` applies the ideal LPF first.
An optional unsharp mask (x + a·(x - x ⊛ g)) boosts the high frequencies that
the interpolation filters attenuate.
"""

from __future__ import annotations

import numpy as np

from .fft import fast_convolve2d, fft2, freq_grid, ifft2
from .filters import filter2d, gaussian, triangle_1d

METHODS = ("Zero-order hold", "Linear interpolation", "Ideal (sinc)")


def crop_to_multiple(x: np.ndarray, f: int) -> np.ndarray:
    h, w = x.shape
    return x[:h - h % f or h, :w - w % f or w]


def ideal_lowpass(x: np.ndarray, f: int) -> np.ndarray:
    """Keep only |ω| < π/f along each axis (the band that survives f× decimation)."""
    k1, k2 = freq_grid(x.shape)
    keep = (np.abs(k1) < x.shape[0] / (2 * f)) & (np.abs(k2) < x.shape[1] / (2 * f))
    return np.real(ifft2(fft2(x) * keep))


def downsample(x: np.ndarray, f: int, antialias: bool = True) -> np.ndarray:
    x = crop_to_multiple(np.asarray(x, dtype=float), f)
    if antialias:
        x = ideal_lowpass(x, f)
    return x[::f, ::f]


def zero_insert(x: np.ndarray, f: int) -> np.ndarray:
    up = np.zeros((x.shape[0] * f, x.shape[1] * f))
    up[::f, ::f] = x
    return up


def upsample_zoh(x: np.ndarray, f: int) -> np.ndarray:
    full = fast_convolve2d(zero_insert(x, f), np.ones((f, f)), "full")
    return full[:x.shape[0] * f, :x.shape[1] * f]


def upsample_linear(x: np.ndarray, f: int) -> np.ndarray:
    xp = np.pad(x, ((0, 1), (0, 1)), mode="edge")   # a right/bottom neighbour for the last ramp
    t = triangle_1d(f)
    full = fast_convolve2d(zero_insert(xp, f), np.outer(t, t), "full")
    return full[f - 1:f - 1 + x.shape[0] * f, f - 1:f - 1 + x.shape[1] * f]


def _pad_spectrum_axis(spec: np.ndarray, new_n: int, axis: int) -> np.ndarray:
    """Place an n-bin spectrum inside new_n bins; the even-n Nyquist bin is split in two."""
    spec = np.moveaxis(spec, axis, -1)
    n = spec.shape[-1]
    out = np.zeros(spec.shape[:-1] + (new_n,), dtype=complex)
    pos = (n + 1) // 2          # bins 0 .. ceil(n/2)-1 are non-negative frequencies
    neg = n // 2                # the last n//2 bins are negative ones
    out[..., :pos] = spec[..., :pos]
    if neg:
        out[..., new_n - neg:] = spec[..., n - neg:]
    if n % 2 == 0 and new_n > n:
        nyq = spec[..., n // 2]
        out[..., n // 2] = nyq / 2
        out[..., new_n - n // 2] = nyq / 2
    return np.moveaxis(out, -1, axis)


def upsample_sinc(x: np.ndarray, f: int) -> np.ndarray:
    h, w = x.shape
    spec = fft2(x)
    spec = _pad_spectrum_axis(spec, h * f, 0)
    spec = _pad_spectrum_axis(spec, w * f, 1)
    return np.real(ifft2(spec)) * f * f


def upsample(x: np.ndarray, f: int, method: str) -> np.ndarray:
    x = np.asarray(x, dtype=float)
    if method == METHODS[0]:
        return upsample_zoh(x, f)
    if method == METHODS[1]:
        return upsample_linear(x, f)
    if method == METHODS[2]:
        return upsample_sinc(x, f)
    raise ValueError(f"unknown method {method!r}")


def unsharp(x: np.ndarray, amount: float, sigma: float = 1.0) -> np.ndarray:
    if amount <= 0:
        return x
    return x + amount * (x - filter2d(x, gaussian(sigma)))
