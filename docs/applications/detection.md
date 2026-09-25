# Object detection (template matching)

Finds every place where the image looks like a template. The course has no machine learning,
so detection here is a **matched filter**: correlation normalised by signal energy.

Code: `playground/core/detection.py`, `playground/ui/apps/detection_page.py`.

## How it works

Correlating the image with a template t is the same as convolving it with the reflected
template, h[m, n] = t[−m, −n]. This is an LTI system whose output peaks where the image
matches t. Raw correlation favours bright regions, so each score is normalised by energies:

```
ncc[m, n] = Σ (x − x̄)(t − t̄)  /  √( E_patch[m, n] · E_template )     ∈ [−1, 1]
```

1. Make the template zero-mean: t₀ = t − t̄. Its energy is E_t = Σt₀².
2. **Numerator**: `fast_correlate2d(x, t₀, "valid")`, an FFT fast convolution. Because
   Σt₀ = 0, this already equals Σ(x − x̄)t₀.
3. **Patch energy**: E_patch = Σx² − (Σx)²/n. Both sums come from `box_sum`
   (accumulate, then difference), so they cost the same for any template size.
4. Divide wherever the denominator is non-negligible; flat patches score 0. Clip to [−1, 1].

The score is 1 exactly when the patch is a brightness- and contrast-shifted copy of the
template (a·t + b with a > 0). It is −1 for an inverted copy.

**Peak picking** (`find_matches`) is greedy:

1. Take the highest score.
2. If it is below the threshold, stop.
3. Otherwise record a match, blank out a template-sized neighbourhood around it, and repeat
   until *Max matches* is reached.

## Using the page

- The default image is **Repeated objects**, and the default template is the first planted
  object. The page finds all 5 copies with score 1.00, even though their brightness and
  contrast differ.
- **Drag a rectangle** (left mouse, at least 3×3 px) on the image to use that region as the
  template. The chosen region is outlined with a blue dashed line.
- **Load template…** uses a separate image file as the template (resized to at most 128 px).
  **Reset** returns to the default template.
- Changing the image resets the template. For a non-sample image the default template is a
  central square about 1/8 of the image.

| Control | Range | Notes |
|---|---|---|
| Threshold | 0.10–1.00 | Minimum ncc for a match |
| Max matches | 1–50 | |
| Add noise σ | 0–80 | Gaussian noise (fixed seed) added to the searched image only, to test robustness |

Display:

- The image with orange match boxes and their scores
- The template
- The **normalised correlation** map (coolwarm, from −1 to 1), with circles on the matches.
  The map's (m, n) is the top-left corner of the template placement.

## API

```python
ncc_map(image, template) -> ndarray            # shape (H − th + 1, W − tw + 1)
find_matches(score, template_shape, threshold=0.8, max_hits=10) -> list[Match]
Match: row, col, height, width, score          # row, col = top-left corner
```
