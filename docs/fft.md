# FFT engine

`playground/core/fft.py` implements the discrete Fourier transform from scratch, following
Ashraf Sir's Lectures 1–4. Every application uses it. It matches `numpy.fft` to about 1e−14
relative error, and `tests/test_fft.py` checks it against the lecture examples.

## Definitions

```
X[k] = Σ_{n=0}^{N−1} x[n] W_N^{kn},      W_N = e^{−j2π/N}
x[n] = (1/N) Σ_{k=0}^{N−1} X[k] W_N^{−kn}
```

## How a length is dispatched (`_fft_any`)

| N | Algorithm | Cost |
|---|---|---|
| 1 | Identity | |
| Power of 2 | Radix-2 decimation in time | N log₂ N |
| Composite, not a power of 2 | General Cooley–Tukey, peeling one odd prime factor at a time | N · Σ factors |
| Prime ≤ 16 | Direct DFT matrix | N² (tiny) |
| Prime > 16 | Bluestein chirp-z | about 3 FFTs of length ≥ 2N − 1 |

All transforms run along the last axis and are vectorised over every other axis. A 2D image
is therefore transformed "all rows at once", not row by row.

### Radix-2 DIT (`_fft_radix2`)

1. Permute the input into **bit-reversed order** (`bit_reversed_indices(8)` gives
   `[0, 4, 2, 6, 1, 5, 3, 7]`).
2. Run log₂ N butterfly stages. At stage size s, each block's first half G and second half H
   combine as

   ```
   X[k]       = G[k] + W_s^k H[k]
   X[k + s/2] = G[k] − W_s^k H[k]
   ```

Twiddle factors and bit-reversal tables are cached for each size.

### General Cooley–Tukey, N = N₁·N₂ (`_fft_cooley_tukey`)

This is Bailey's four-step form of the tabular view:

1. Load x column-major into an N₁ × N₂ matrix: entry (n₁, n₂) = x[N₁n₂ + n₁].
2. Take an N₂-point DFT of every row (recursively, so the remaining power of 2 uses radix-2).
3. Multiply entry (n₁, k₂) by the twiddle W_N^{n₁k₂}.
4. Take an N₁-point DFT down every column, and read the result row-major: k = N₂k₁ + k₂.

N₁ is the smallest odd prime factor. Small factors (≤ 16) use a DFT-matrix product;
larger ones use Bluestein.

### Bluestein (`_fft_bluestein`)

Uses kn = (k² + n² − (k − n)²)/2:

```
X[k] = W_{2N}^{k²} · Σ_n (x[n] W_{2N}^{n²}) · W_{2N}^{−(k−n)²}
```

This is a linear convolution of a[n] = x[n]·chirp with the conjugate chirp b[n]. It is
computed with radix-2 FFTs of length M = next power of 2 ≥ 2N − 1. The negative-index half of
b is wrapped to the end of the buffer (the circular wrap, used on purpose). For precision,
n² is reduced mod 2N before the exponential.

### Inverse

`IDFT{X} = conj(DFT{conj(X)}) / N`. The inverse reuses the forward algorithms.

## Public API

| Function | Description |
|---|---|
| `fft(x, axis=-1)`, `ifft(x, axis=-1)` | 1D DFT / IDFT along an axis; complex output |
| `fft2(x)`, `ifft2(x)` | 2D over the last two axes: rows first, then columns |
| `fftshift(x)`, `ifftshift(x)` | Move bin 0 to the centre and back (last two axes) |
| `freq_grid(shape)` | Signed bin indices (k ≤ N/2 → k, otherwise k − N) for every 2D bin |
| `log_spectrum(img)` | Centred log(1 + \|X\|), the standard spectrum picture |
| `next_pow2(n)`, `is_pow2(n)` | Power-of-2 helpers |
| `good_size(n)` | Smallest length ≥ n with prime factors in {2, 3, 5} only |
| `bit_reversed_indices(n)` | Radix-2 input order |
| `kernel_otf(kernel, shape)` | DFT of a kernel zero-padded to `shape`, with its centre rolled to (0, 0) |
| `fast_convolve2d(x, h, mode)` | Convolution via DFT products (below) |
| `fast_correlate2d(x, t, mode="valid")` | Cross-correlation = convolution with t flipped |

## Fast convolution (`fast_convolve2d`)

Multiplying DFTs gives **circular** convolution. Zero-padding both signals to N ≥ L + M − 1
per axis leaves room for the tail, so circular equals linear. The padded size is
`good_size(L + M − 1)`: a 2·3·5-smooth length, so the mixed-radix path stays fast without
jumping to the next power of 2.

| Mode | Output | Equivalent direct call |
|---|---|---|
| `"full"` | (H + k_h − 1) × (W + k_w − 1) | numpy `convolve` "full" |
| `"same"` | H × W, kernel centred | `convolve2d(x, h, padding="zero")` |
| `"valid"` | (H − k_h + 1) × (W − k_w + 1) | `convolve2d(x, h, padding="valid")` |
| `"circular"` | H × W, no padding, wrap kept | `convolve2d(x, h, padding="circular")` |

**Two real images for the price of one.** Passing a complex `x = x₁ + j·x₂` with a real
kernel returns `(x₁ ⊛ h) + j·(x₂ ⊛ h)`, by linearity. Portrait mode uses this to blur an
image and its mask in one pass.

## Performance

Measured on the development machine:

- 2D FFT of 512×512: about 0.1 s
- 2D FFT of 300×400: about 0.06 s
- 2D FFT of 576×576: about 0.16 s
