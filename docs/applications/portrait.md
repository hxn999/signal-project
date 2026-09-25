# Portrait mode (lens blur)

A synthetic shallow depth of field: the subject stays sharp and the background is blurred the
way a wide-aperture lens would blur it.

Code: `playground/core/portrait.py`, `playground/ui/apps/portrait_page.py`.

## How it works

An out-of-focus lens spreads each point into a disc, so defocus is **convolution with a
pillbox** h = `disc(r)`. This is a 2D rect in the radius, whose spectrum has sinc-like
ripples that give the "bokeh" look. The radius grows with distance from the focal plane.

1. A per-pixel **blur amount** a ∈ [0, 1] (0 means in focus) comes from one of the three
   subject sources below.
2. a is scaled to [0, L − 1] for L **layers**. Layer ℓ uses a disc of radius
   r_ℓ = r_max · ℓ/(L − 1). Pixels get soft layer weights w_ℓ = max(0, 1 − |a − ℓ|), which
   sum to 1.
3. Each layer is blurred with **normalised convolution**:

   ```
   blurred_ℓ = (x · m_ℓ ⊛ disc) / (m_ℓ ⊛ disc)
   ```

   where m_ℓ selects pixels at least as far away as this layer. The sharp subject therefore
   does not bleed into the blurred background (no halo). Numerator and denominator are
   computed in one FFT pass by packing them into one complex image.
4. The output is Σ w_ℓ · blurred_ℓ. Pixels with a = 0 come through untouched (layer 0 has
   radius 0).

Convolutions use edge-replicated padding and FFT fast convolution.

## Subject sources

| Source | How the blur amount is made | Interaction |
|---|---|---|
| **Ellipse (click subject)** | a = 1 − (ellipse mask ⊛ Gaussian feather) | Click the original image to move the ellipse. Size is set by height % and width %. |
| **Sharpness map (auto)** | Local energy of the Laplacian, Σ_window (∇²x)², normalised and thresholded. High-frequency energy is large only where the photo is already in focus. Then feathered. | None |
| **Stereo depth (click focus)** | Uses the disparity map from the [Stereo vision](stereo.md) tab: a ∝ \|d − d_focus\|, feathered. For a thin lens focused at Z_f the blur diameter is ∝ \|1/Z − 1/Z_f\|, and d = f·B/Z, so blur ∝ \|d − d_focus\|. | Click to choose the focus point. d_focus is the median disparity of a 5×5 patch there. Run the Stereo tab first; the page updates when a new stereo result arrives. |

## Controls

| Control | Range | Used by |
|---|---|---|
| Subject from | 3 sources | |
| Ellipse height / width | 5–100 % of the image | Ellipse |
| Sharpness window | 3–61 px | Sharpness |
| Sharpness threshold | 0.01–1.0 (fraction of max) | Sharpness |
| Feather σ | 0–20 px | All |
| Max blur radius | 1–30 px | All |
| Blur layers | 2–10 | All |

Display: the original (with the ellipse outline or focus cross), the blur-amount map (magma),
and the result. Results card: subject centre, focus disparity or sharp-area fraction, % of
pixels in focus, and the disc radii used.

Speed: about 0.4 s at 256 px and about 2 s at 512 px with r = 8 and 5 layers.

## API

```python
ellipse_mask(shape, center, axes) -> ndarray             # 1 inside, center/axes = (row, col)
sharpness_map(img, window=15) -> ndarray                 # in [0, 1]
sharpness_mask(img, window=15, threshold=0.2) -> ndarray
feather(mask, sigma) -> ndarray
amount_from_mask(mask, feather_sigma=4.0) -> ndarray
amount_from_disparity(disparity, focus, span=None, feather_sigma=1.0) -> ndarray
lens_blur(img, amount, max_radius=8.0, layers=5) -> ndarray
```
