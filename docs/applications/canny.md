# Canny edge detection

The classic five-stage edge detector, built from convolutions. The page shows every
intermediate stage.

Code: `playground/core/edges.py`, `playground/ui/apps/canny_page.py`.

## Pipeline

1. **Smooth**: x ⊛ Gaussian(σ), using `filter2d` with edge replication. Differentiation
   amplifies high-frequency noise, so a low-pass LTI system comes first. σ = 0 skips this
   step.
2. **Differentiate**: g_x = s ⊛ Sobel X and g_y = s ⊛ Sobel Y (3×3, with the playground's
   own `convolve2d`, replicate padding). These are differencing kernels with DC gain ΣΣh = 0.
3. **Magnitude and direction**: |∇| = √(g_x² + g_y²), normalised so its maximum is 1.
   θ = atan2(g_y, g_x) mod 180°.
4. **Non-maximum suppression**: θ is rounded to 0°, 45°, 90° or 135°. A pixel survives only
   if its magnitude beats both neighbours along that direction, which thins edges to one
   pixel. The comparison is strict on one side, so of two equal pixels straddling a
   symmetric step only one survives.
5. **Double threshold and hysteresis**:
   - Pixels ≥ *high* are **strong** edges.
   - Pixels ≥ *low* are **weak**.
   - Weak pixels are kept only if they connect to a strong pixel through 8-connected
     neighbours. This is done by repeated one-pixel growth restricted to candidate pixels,
     until nothing changes.

Thresholds are fractions of the largest gradient magnitude. If *low* > *high* they are
swapped.

## Controls

| Control | Range | Default |
|---|---|---|
| Gaussian σ | 0–6 | 1.4 |
| Low threshold | 1–99 % | 8 % |
| High threshold | 1–100 % | 20 % |

## Display (2 × 3)

1. The smoothed image
2. The gradient magnitude |∇| (inferno)
3. The direction θ as hue (hsv), masked where |∇| < 0.05
4. The result of non-max suppression
5. Strong pixels in white, weak in grey
6. The final edges after hysteresis

Results card: counts of strong, weak and kept-weak pixels, total edge pixels (and their
share of the image), and the thresholds.

Things to try:

- Raise σ to suppress texture edges.
- Lower *high* to pick up faint edges.
- Widen the gap between *low* and *high* to close breaks in contours.

## API

```python
canny(img, sigma=1.4, low=0.1, high=0.25) -> CannyResult
CannyResult: smoothed, gx, gy, magnitude, direction, suppressed, strong, weak, edges
non_max_suppression(mag, direction) -> ndarray
hysteresis(strong, weak) -> ndarray[bool]
```
