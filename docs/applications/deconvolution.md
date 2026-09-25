# Deconvolution (deblurring)

Recovers a sharp image from a blurred one when the blur kernel is known: blurry → stable.

Code: `playground/core/deconvolution.py`, `playground/ui/apps/deconv_page.py`.

## How it works

Blur is an LTI system, y = x ⊛ h (+ noise). The **convolution theorem** gives
Y[k] = X[k] · H[k], so dividing spectra undoes the blur. This is the inverse filter,
X̂ = Y / H. Two guards make it usable, and both are plain spectrum arithmetic:

```
G[k] = H*[k] / (|H[k]|² + K)      where |H[k]| ≥ ε
G[k] = 0                          where |H[k]| < ε   (and always where H = 0 exactly)
X̂ = IDFT{ Y · G }
```

- **ε (cut)**: where |H| ≈ 0 the blur erased that frequency. Dividing by it only amplifies
  noise, so those bins are dropped.
- **K (regularise)**: 1/H = H*/|H|². Adding K to the denominator caps the gain at about
  1/(2√K), a smooth version of the same idea.
- **K = ε = 0** is the pure inverse. It is exact with no noise, and it explodes with even a
  little noise.

**The circular-convolution lesson.** Multiplying DFTs performs circular convolution, but a
real photo is not periodic. With **Mirror-pad before the DFT** on, the image is padded
symmetrically by the kernel size first and cropped afterwards, so the wrap does not drag the
opposite edge into the result. To see the exact case, tick **Circular blur** and untick
padding: the blur and its inverse then share the same periodic model.

The kernel's spectrum comes from `kernel_otf`, which zero-pads the PSF and rolls its centre
to (0, 0).

## Blur kernels (PSF)

| Kind | Size means | Default | Spectrum |
|---|---|---|---|
| Gaussian | σ | 2 | Gaussian; never exactly zero, but tiny at high frequency |
| Motion | length (px), plus an angle | 12 | Sinc-like along the motion, with exact zeros |
| Defocus (disc) | radius | 3 | Ring-shaped (jinc-like) zeros |
| Box | width | 5 | Separable sinc with exact zeros |

Choosing a kind resets the size to its default.

## Controls

| Control | Notes |
|---|---|
| Input | **Sharp image → blur it here** (synthetic, with PSNR scores) or **Already blurry → restore** (restores the chosen image with the PSF you pick) |
| Blur PSF h, Size, Angle | Angle is for Motion only |
| Noise σ | Synthetic mode only. Gaussian noise with a fixed seed. |
| Circular blur | Synthetic mode only. Blur with the periodic model. |
| ε | 0–0.5 (default 0) |
| K | 0–1 (default 0.002) |
| Mirror-pad before the DFT | Default on |

Display: original, blurred, restored; the PSF; log₁₀|H| (blur response); log₁₀|G|
(restoration gain). Results card: the PSF, % of bins cut by ε, min |H|, max gain |G|, and
PSNR of the blurred and restored images (synthetic mode).

With the defaults (Textured scene, Gaussian σ = 2, noise 0.5, K = 0.002), PSNR goes from
22.8 dB to 28.1 dB.

This page does not estimate the blur (no blind deconvolution). For a real blurry photo you
choose the PSF type and size yourself.

## API

```python
make_psf(kind, size, angle=0.0) -> ndarray                    # PSF_KINDS
blur(x, psf, circular=False) -> ndarray
degrade(x, psf, noise_std=0.0, circular=False, seed=0) -> ndarray
inverse_filter(y, psf, eps=1e-3, k=0.0, pad=True) -> DeconvResult
DeconvResult: restored, otf_mag, gain_mag (both centred), zeroed (fraction of bins cut)
```
