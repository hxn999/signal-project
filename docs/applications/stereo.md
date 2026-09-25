# Stereo vision

Computes depth from two views taken a small horizontal distance apart.

Code: `playground/core/stereo.py`, `playground/ui/apps/stereo_page.py`.

## How it works

Two cameras a baseline B apart, with focal length f, see a point at depth Z shifted
horizontally by the **disparity** d = f·B / Z. Near objects shift more.

For every candidate d = 0 … D:

1. **Shift** the right view by d. This is a pure time shift, R_d[m, n] = R[m, n − d], with
   the edge replicated where n − d < 0.
2. **Compare** it with the left view through the **energy** of the difference, summed over a
   block by a box filter (`box_sum`, "same" mode):

   ```
   C_d[m, n] = Σ_block ( L[m, n] − R[m, n − d] )²
   ```

Each pixel takes the d with the lowest cost (winner takes all). Depth is Z = f·B / d, with d
clamped to at least 0.5 to avoid dividing by zero. The whole search costs D + 1 box sums, and
each box sum costs O(1) per pixel.

## Synthetic stereo pairs

Most people don't have a calibrated stereo camera, so **Synthetic pair from image** renders a
right view from any image:

- `default_disparity_layers(shape, max_disp)` builds a scene with three depths:
  - background: d = max/6
  - a mid rectangle: d = max/2
  - a near disc: d = max
- `synthetic_pair(img, disparity)` treats the image as the left view. Each pixel lands at
  column n − d in the right view. Pixels are painted far to near so nearer surfaces occlude,
  and uncovered holes take the background shift.

Because the true disparity is known, the page reports accuracy. With the defaults
(Textured scene), about 95 % of interior pixels are exactly right. Errors cluster in
occlusions and at the left edges of objects, where one view sees background that the other
cannot.

Matching needs texture: flat regions are ambiguous. Use **Textured scene** (the default)
rather than Shapes.

## Controls

| Control | Range | Notes |
|---|---|---|
| Stereo pair | Synthetic / Load left + right | File mode hides the Image card |
| Left… / Right… | | File mode. Both images must be the same size (use a rectified pair). They load at the Image card's resolution. |
| Scene disparity (near) | 2–40 px | Synthetic mode: the near disc's true disparity |
| Search range | 1–64 px | D, the largest disparity tried |
| Block size | 3–31 px (odd) | Bigger is smoother but blurs object borders |
| f·B | 1–10000 | Scale of the depth map (arbitrary units) |

## Display (2 × 3)

- Left view, right view, and |L − R| (the shift is visible)
- The estimated disparity
- The true disparity (synthetic mode) or the matching cost √C (file mode)
- Depth Z (magma, near is bright, clipped at the 98th percentile)

Results card: image size, disparities tried, block size, then exact and within-1-px accuracy
(synthetic mode) or the file names.

Every run publishes the left image and disparity map to the shared `AppContext`. The
[Portrait mode](portrait.md) tab's **Stereo depth** source uses them.

## API

```python
shift_right(x, d) -> ndarray
disparity_map(left, right, max_disp=16, block=7, focal_baseline=100.0) -> StereoResult
StereoResult: disparity, cost, depth
default_disparity_layers(shape, max_disp=12) -> ndarray
synthetic_pair(img, disparity) -> (left, right)
```
