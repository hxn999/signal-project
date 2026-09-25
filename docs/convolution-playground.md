# Convolution playground

The core of the app: choose an input and a kernel, set stride and padding, and watch
`y = x ⊛ h` being computed one output sample at a time.

Code: `playground/core/convolution.py`, `playground/core/kernels.py`,
`playground/core/image_io.py`, `playground/state.py`, and the `playground/ui/` panels
`input_panel.py`, `kernel_panel.py`, `compute_panel.py`, `step_view.py`,
`animation_bar.py`, `matrix_grid.py`, `result_view.py`.

## Input (sidebar → Input card)

A segmented control switches between **Sketch grid** and **Image**. Only one is active at a
time (`PlaygroundState.source` is `"sketch"` or `"image"`).

### Sketch grid

| Control | Behaviour |
|---|---|
| Size (rows × cols) | 2 to 64 each. Resizing keeps the top-left values and fills new cells with 0. |
| Brush value | −999 to 999. The value painted by a left-drag. |
| Clear | Sets every cell to 0. |
| Random | Random integers 0–9. |
| Patterns ▾ | Square, Ring, Cross, Diagonal, Checkerboard, Vertical edge, Gradient (drawn with the brush value), then **2D Impulse** and **2D Step** (see [LTI analysis](lti-analysis.md)). |

You draw directly on the input grid in the Step-by-step tab:

- **Left-drag** paints the brush value.
- **Right-drag** erases (paints 0).
- **Double-click** opens an editor for an exact value. Enter commits and moves to the next cell.
- **Hover** shows the cell's value in a tooltip.

### Image

**Upload image…** opens PNG, JPG, BMP, GIF, TIFF or WebP files. The image is converted to a
grayscale intensity matrix in [0, 255] (`image_io.to_intensity`):

- EXIF orientation is applied.
- Transparency is composited onto white.
- The image is resized with Lanczos so its longest side is the chosen **Resolution**:
  16, 32 (default), 64, 128 or 256 px. Changing the resolution reloads the same file.

Small resolutions keep the step-by-step view readable; large ones render as pixels.
Loading an image switches to the Result map tab.

## Kernel (sidebar → Kernel card)

### Presets (`core/kernels.py`)

Every preset takes an odd size n from 3 to 9. The size spin boxes step by 2 while a preset
is selected.

| Preset | Category | Definition |
|---|---|---|
| Identity | Basic | Centred unit impulse δ |
| Box blur | Blur | All entries 1/n² |
| Gaussian blur | Blur | Outer product of binomial rows, normalised (3×3 = [1 2 1]ᵀ[1 2 1]/16) |
| Sharpen | Sharpen | 3×3: [[0,−1,0],[−1,5,−1],[0,−1,0]]; larger: unsharp mask 2δ − Gaussian |
| Laplacian | Edge detection | All −1, centre n² − 1 (DC gain 0) |
| Sobel X / Y | Edge detection | Binomial smoothing ⊗ binomial derivative; Y is the transpose of X |
| Prewitt X / Y | Edge detection | Ones ⊗ ramp −n/2 … n/2 |
| Emboss | Emboss | h[i,j] = i + j − (n − 1), centre 1 |

`make_preset(name, n)` raises `KeyError` for unknown names and `ValueError` for even or
too-small sizes.

### Custom kernels

- Choose **Custom**, or edit any value of a preset (this turns it into a custom kernel).
- Size is 1 to 9 per side, and rectangular kernels are allowed. Resizing grows or shrinks
  around the centre so the origin stays put (`resize_centered`).
- **Double-click** a cell to edit it; Enter jumps to the next cell.
- **Normalize** divides by ΣΣh so the kernel has unit DC gain (skipped when the sum is 0).
- **Zero** clears every entry.
- The label under the grid shows ΣΣh.
- Values use a diverging colour map: blue is negative, orange is positive.

## Computation (sidebar → Computation card)

| Control | Values |
|---|---|
| Stride (rows × cols) | 1 to 8 each |
| Padding | Valid (no padding), Zero, Reflect, Replicate (edge), Circular (wrap) |
| Mode | Convolution (flip kernel) or Cross-correlation (no flip). See [LTI analysis](lti-analysis.md). |

The card shows the input size, the padded size, the output size and the number of steps,
plus an error message when the kernel does not fit.

### What is computed

`convolve2d(x, k, stride, padding, flip)` in `core/convolution.py`:

```
y[m, n] = Σ_i Σ_j  x_pad[m·s_r + i, n·s_c + j] · k_applied[i, j]
k_applied = k[::-1, ::-1]   (convolution)   or   k   (cross-correlation)
```

- **Padding amounts** ("same"-style): top = ⌊(k_h − 1)/2⌋ and bottom = k_h − 1 − top, so
  even kernels get the extra row at the bottom (same for columns).
- **Output size**: `((H + top + bottom − k_h) // s_r + 1, (W + left + right − k_w) // s_c + 1)`.
- **Valid** uses no padding, so the output shrinks by k − 1.
- A kernel larger than the (padded) input raises `ConvolutionError`, which is shown in the
  UI instead of an output.

The returned `ConvResult` keeps the input, kernel, applied kernel, padded input, padding
amounts, stride, mode and output. `ConvResult.step(i)` rebuilds step i: output position,
window origin, the patch under the window, the element-wise products, and their sum.

## Step-by-step tab

Three panes: **Input x[m, n]** (padded, with padding cells marked), the **kernel** as
applied (flipped for convolution), and **Output y[m, n]**. The operator glyph is ⊛ for
convolution and ⋆ for correlation.

During the animation:

- The sliding window is outlined on the padded input.
- The output reveals samples in raster order and highlights the current one.
- The breakdown card shows the full equation, for example
  `y[m, n] = Σ x_pad[…]·h̃[i, j] = a·b + c·d + … = value`. At most 12 terms are written out;
  the rest are summarised.

Grids with small cells show their values in the tiles. Large matrices (images) are drawn as
pixels instead.

### Animation controls (`animation_bar.py`)

| Control | Shortcut | Action |
|---|---|---|
| Reset | Home | Back to "ready" (no output shown) |
| Step back / forward | ← / → | One output sample |
| Play / pause | Space | Animate at the chosen speed |
| Finish | End | Show the complete output |
| Scrubber | | Jump to any step |
| Speed | | 1–60 ticks per second |
| ×1 / ×10 / ×100 / ×1000 | | Steps per tick. Chosen automatically for each new input: ×1 up to 400 steps, ×10 up to 4000, otherwise ×100. |

The animation cursor lives in `PlaygroundState.step`: −1 means reset, 0 … N−1 is an active
step, and N means finished. Any change of input, kernel or parameters recomputes the result
and jumps to "finished".

## Result map tab (`result_view.py`)

Matplotlib rendering of the input (always grayscale; 0–255 for images) and the output, each
with a colour bar, plus the output's min, max and mean.

| Control | Options |
|---|---|
| Colormap | Grayscale, Heatmap (inferno), Viridis, Magma, Diverging (coolwarm) |
| Output scaling | Min–max, Clip to 0–255, Absolute value \|y\|, Symmetric ±max |

Use **Absolute value** or **Symmetric** for edge kernels whose output is signed.
