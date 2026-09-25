# LTI system analysis

These features (added in v0.2) treat the kernel h[i, j] as the impulse response of a 2D LTI
system and test its properties.

Code: `playground/core/analyzer.py`, `playground/ui/analyzer_panel.py`,
`playground/ui/compute_panel.py`, and the pattern menu in `playground/ui/input_panel.py`.

## Reflect-and-shift: convolution vs cross-correlation

The Computation card's **Mode** picks the operation:

| Mode | Kernel actually slid | Glyph | Equation label |
|---|---|---|---|
| Convolution | h[−i, −j] (reflected, then shifted) | ⊛ | h̃ = flipped h |
| Cross-correlation | h[i, j] (shifted only) | ⋆ | no flip |

The state computes both results on every change (`result` and `result_alt`), and the card
reports **max |conv − corr|**:

- For a symmetric kernel (h[i, j] = h[−i, −j], see `is_symmetric`) the two are identical, and
  the card says so in blue.
- Otherwise the maximum difference is shown in orange. Sobel, Prewitt and Emboss are good
  examples.

API:

- `is_symmetric(kernel) -> bool`
- `conv_corr_difference(out_conv, out_corr) -> float | None`: None if either output is
  missing or their shapes differ.

## Causality (Analysis card)

**Raster-scan ordering**: the output is produced row by row, left to right. The kernel's
origin is its centre `(rows // 2, cols // 2)`. The system is causal when every non-zero tap
lies at or after the origin in raster order:

```
row > origin_row   or   (row == origin_row  and  col >= origin_col)
```

For a non-causal kernel the card shows the **minimum origin shift (a, b)**: the offset from
the centre to the first non-zero tap in raster order. Moving the origin there makes every tap
causal. For example, a 3×3 box has its first tap at (0, 0) and origin (1, 1), so
(a, b) = (−1, −1).

API: `check_causality(kernel) -> CausalityResult(is_causal, origin, shift)`, where `shift`
is None when the kernel is already causal. An all-zero kernel counts as causal.

## BIBO stability (Analysis card)

A 2D LTI system is BIBO stable iff S = ΣΣ|h[i, j]| < ∞. That always holds for a finite
kernel, so the card always reports **stable** and then shows the numbers:

- **S** = ΣΣ|h|
- **B** = max|x| (the input bound)
- **Bound**: |y| ≤ B·S
- **Actual** max|y| from the computed output, with a ✓ when it is within the bound

The bound is reached when the input's signs line up with the kernel's.

API: `compute_bibo(kernel, input, output) -> BIBOResult(s_abs, b_max, y_bound,
y_actual_max, is_bibo_stable)`.

## DC gain and classification (Analysis card)

G = ΣΣh[i, j] is the response to a constant input (frequency 0).

| G | Class | Meaning |
|---|---|---|
| ≠ 0 | **Averaging** | Passes the mean; low-pass-like (blur, identity, sharpen) |
| ≈ 0 (\|G\| < 1e−9) | **Differencing** | Removes the mean; high-pass-like (Laplacian, Sobel, Prewitt) |

API: `dc_gain(kernel) -> float`, `kernel_classification(kernel) -> "Averaging" | "Differencing"`.

The Kernel card's **Normalize** button scales the kernel so that G = 1.

## Impulse and step response mode

Two entries at the bottom of the sketch grid's **Patterns ▾** menu:

- **2D Impulse**: δ[m, n], a single 1 at the grid centre. Convolving gives y = h. The output
  grid shows the kernel itself, placed at the impulse. This demonstrates that the kernel *is*
  the impulse response. With zero padding the kernel appears unflipped, because the flip and
  the reflection of the impulse cancel.
- **2D Step**: u[m, n] = 1 for m ≥ centre and n ≥ centre. The output is the accumulated
  (running-sum) response. Far inside the step it settles to the DC gain G.

Try the step with Box blur (it settles at G = 1) and with the Laplacian (it settles at 0 and
responds only at the step's edges).
