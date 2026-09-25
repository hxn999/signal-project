# Applications tab: shared parts

The **Applications** tab holds seven pages:

- [Compression](compression.md)
- [Object detection](detection.md)
- [Portrait mode](portrait.md)
- [Deconvolution](deconvolution.md)
- [Canny edges](canny.md)
- [Stereo vision](stereo.md)
- [Super resolution](superres.md)

The convolution sidebar is hidden while this tab is open, because each page has its own
controls.

Code: `playground/ui/apps/` (`base.py`, `applications_view.py`, one `*_page.py` per
application), plus `playground/core/filters.py` and `playground/core/samples.py`.

## Page layout

Every page is an `AppPage` with a control column on the left and a Matplotlib figure on the
right. The control column has four cards:

| Card | Contents |
|---|---|
| **Image** | Image source picker (below). Hidden on pages or modes that bring their own image, such as stereo file mode and portrait stereo-depth mode. |
| **Parameters** | Page-specific controls. Rows that don't apply to the current mode are hidden. |
| **Results** | A table of metrics from the last run. |
| **How it works** | A short explanation that names the syllabus ideas used. |

### When pages recompute

- Any parameter change schedules a recompute after a 250 ms pause, so dragging a spin box
  doesn't queue many runs.
- A page only computes while it is visible. Switching to it runs any pending update.
- The cursor shows "busy" during a run.
- Errors (such as a kernel larger than the image) are shown in red on the figure instead of
  crashing the app.

## Image source

| Option | Meaning |
|---|---|
| Sample · … | One of the built-in synthetic images (below), generated at the chosen size |
| Playground input | The sidebar's current input. Sketch values are rescaled to 0–255. It updates when the playground input changes. |
| Image file | A file chosen with **Load image…** (same formats as the playground) |

**Resolution** (128, 256 default, or 512 px, longest side) applies to samples and files. The
hint underneath shows the image name and its matrix size.

## Sample images (`core/samples.py`)

All samples are deterministic (fixed random seeds) and grayscale in [0, 255]:

| Sample | Content | Best for |
|---|---|---|
| Shapes | Gradient background, disc, square, triangle, stripes, mild texture | Compression, Canny, portrait |
| Textured scene | Shapes with strong random texture | Deconvolution, stereo |
| Repeated objects | A ring-and-star template planted 5 times with different brightness and contrast | Object detection |
| Checkerboard | 16 × 16 squares | Edges, aliasing |
| Zone plate | cos(π r² / 1.5N): frequency rises outward to about 0.94π in the corners | Super resolution and aliasing |

Helpers: `SAMPLES` (name → generator), `pattern_template(size)` and
`pattern_positions(size)` (the planted objects' top-left corners).

## Filter helpers (`core/filters.py`)

| Function | Description |
|---|---|
| `gaussian(sigma, radius=None)` | Sampled Gaussian, radius ⌈3σ⌉, DC gain 1 (σ ≤ 0 gives an impulse) |
| `disc(radius)` | Pillbox (2D rect in the radius): the defocus impulse response |
| `box(n)` | n×n average |
| `triangle_1d(f)` | First-order-hold pulse of half-width f, equal to rect ⊛ rect |
| `motion(length, angle_deg)` | Straight-line camera-shake kernel |
| `filter2d(x, k, boundary)` | Same-size convolution with a playground padding mode (`"replicate"`, `"reflect"`, `"zero"`, `"circular"`), via fast convolution. Matches `convolve2d` exactly. |
| `box_sum(x, h, w, mode)` | Sum over every h×w window, computed as "accumulate then difference" (see below). `"valid"` or `"same"`. |
| `mse(a, b)`, `psnr(ref, test, peak=255)` | Error metrics; PSNR = 10 log₁₀(peak² / MSE), ∞ when the images are identical |

`box_sum` ties back to the unit step. A box is rect = u[n] − u[n − B], so convolving with it
is the same as taking a running sum (the step response of an accumulator) and then a
difference. A 2D cumulative sum does this at O(1) cost per pixel, whatever the window size.
