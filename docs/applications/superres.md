# Super resolution

Upscales an image by reconstructing it from its samples, straight out of the sampling
lecture. It also demonstrates aliasing.

Code: `playground/core/superres.py`, `playground/ui/apps/superres_page.py`.

## How it works

Upscaling ×f means reconstructing the underlying band-limited image and re-sampling it on a
grid f times finer. Every method is "insert f − 1 zeros between samples, then low-pass
filter". Zero insertion creates spectral copies, and the filter decides how many survive.

| Method | Impulse response | Frequency response | Look |
|---|---|---|---|
| **Zero-order hold** | rect of width f | ~ sinc: leaks copies | Blocky |
| **Linear interpolation** | triangle = rect ⊛ rect, width 2f − 1 | ~ sinc²: less leakage | Smooth but soft |
| **Ideal (sinc)** | sinc, brick-wall cutoff π/f | Exactly 1 inside the band, 0 outside | Sharpest; rings at edges |

Implementation details:

- **ZOH and linear**: zero-insert, then FFT fast convolution with `ones(f, f)` or
  `outer(triangle, triangle)`, and crop to align the samples. For linear interpolation the
  image is first edge-padded by one pixel on the bottom and right, so the last ramp has a
  neighbour to interpolate towards.
- **Ideal sinc**: done exactly in the DFT domain. Take the 2D DFT, place the n bins inside a
  zero spectrum of n·f bins (positive frequencies at the start, negative ones at the end),
  inverse-transform, and scale by f². For even n the Nyquist bin is split half-and-half
  between +n/2 and −n/2 so the result stays real and symmetric. This treats the image as
  periodic, so strong edges at the border can ring.

A band-limited image is reproduced exactly by the sinc method, and a test checks this.

## Simulate mode and aliasing

**Simulate: downsample, then upscale** first makes a low-resolution copy, so the upscaled
result can be scored (PSNR) against the original:

- **With the anti-alias LPF** (`ideal_lowpass`): frequencies with |ω| ≥ π/f are removed
  before keeping every f-th sample. This is the Nyquist condition for the new rate.
- **Without it**: frequencies above the new Nyquist limit **fold back** (alias). The default
  **Zone plate** sample makes this obvious: false rings appear in the low-resolution image,
  and no reconstruction method can remove them.

**Upscale the image itself** instead enlarges the chosen image directly, capped at 1024 px.

An optional **unsharp mask**, x + a(x − x ⊛ g) with σ = 1, re-boosts the high frequencies
that the interpolation filters attenuate.

## Controls

| Control | Range | Default |
|---|---|---|
| Mode | Simulate / Upscale | Simulate |
| Factor f | 2–8 | 2 |
| Anti-alias LPF before downsampling | on / off | on (Simulate mode only) |
| Unsharp amount | 0–3 | 0 |

## Display (2 × 4)

- **Top row**: the original (or the input), then ZOH, linear and sinc results, each with its
  PSNR in Simulate mode.
- **Bottom row**: the low-resolution samples (or the input spectrum), then the log spectrum
  of each result. The ZOH spectrum shows the leaked copies, and the sinc spectrum shows a
  clean square band.

Results card: low-resolution and upscaled sizes, and the PSNR per method.

## API

```python
METHODS = ("Zero-order hold", "Linear interpolation", "Ideal (sinc)")
crop_to_multiple(x, f), ideal_lowpass(x, f), downsample(x, f, antialias=True)
zero_insert(x, f), upsample_zoh(x, f), upsample_linear(x, f), upsample_sinc(x, f)
upsample(x, f, method), unsharp(x, amount, sigma=1.0)
```
