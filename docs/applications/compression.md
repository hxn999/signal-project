# Image compression

Transform coding with the 2D DFT: the idea behind JPEG, using the Fourier transform from the
course instead of the DCT.

Code: `playground/core/compression.py`, `playground/ui/apps/compression_page.py`.

## How it works

1. **Split** the image into B×B blocks. The edges are padded by replication up to a multiple
   of B. "Whole image" uses a single block.
2. **Transform** every block with a 2D DFT (rows, then columns). All blocks are transformed
   in one batched call.
3. **Discard** information, using one of two methods:
   - **Keep largest coefficients**: keep the top K % of bins by |X[k]| across the whole
     image, and zero the rest. Kept bins are made conjugate-symmetric (if X[k] is kept, so is
     X[−k]), so the inverse is exactly real.
   - **Frequency-weighted quantisation**: round each bin's real and imaginary parts to a
     multiple of a step q(k). The step grows linearly with the normalised radial frequency,
     `q = step · √(B_h B_w)/8 · (1 + 4r)`, where r goes from 0 at DC to about 1.4 in the
     corners. Fine detail is stored coarsely, and most high-frequency bins round to 0.
     Rounding is symmetric, so conjugate symmetry is preserved automatically.
4. **Rebuild** each block with the inverse DFT and crop off the padding.

## Why the numbers are honest

- **Storage (conjugate symmetry).** A real block has X[−k] = X[k]*. A kept conjugate pair
  therefore costs 2 real numbers, and a self-conjugate bin (DC or Nyquist) costs 1. So *the
  number of real values to store equals the number of kept bins*, and a full block needs B²
  numbers, the same as its pixels. **Compression ratio** = pixels / kept bins. Entropy coding
  of the surviving values is not modelled.
- **Energy (Parseval).** Σ|x|² = (1/N) Σ|X|², so "spectral energy kept" is also "signal
  energy kept". The test suite checks that the reconstruction's energy matches this figure.

## Controls

| Control | Range | Notes |
|---|---|---|
| Method | Keep largest / Quantise | |
| Block size | 8, 16, 32, 64, whole image | Small blocks adapt to local detail but show blocking artefacts |
| Keep | 0.1–100 % | "Keep largest" only. 100 % is lossless. |
| Quantiser step | 1–500 | "Quantise" only. Larger means smaller and worse. |

## Display

- **Original** and **Reconstruction**, with the ratio in the title
- **Error |x − x̂|** (magma colour map, with a colour bar)
- **Kept bins per block**: each block's mask, centred so DC is in the middle of every tile.
  Smooth blocks keep only a few central bins; edge blocks keep a streak perpendicular to the
  edge.

Results card: pixels, stored numbers, compression ratio, energy kept, MSE, and PSNR (∞ when
lossless).

## API

```python
compress(img, block=8, method=METHODS[0], keep=0.1, step=20.0) -> CompressionResult
# block=None means one block covering the whole image
CompressionResult: reconstruction, kept_map, kept, total, energy_kept, mse, psnr, block, ratio
METHODS = ("Keep largest coefficients", "Frequency-weighted quantisation")
```

Example (Shapes sample, 256 px, 8×8 blocks, keep 10 %): ratio 10 : 1, 99.996 % of the energy
kept, PSNR ≈ 50 dB.
