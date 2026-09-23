# Interactive 2D Convolution Playground

CSE 219 — Signals and Linear Systems. A desktop app (PySide6 / Qt 6) for exploring
2D convolution: the kernel is treated as the impulse response of a 2D LTI system and
the convolution is animated one output sample at a time.

**Version 0.2** adds correlation comparison, causality & BIBO analysis, and
impulse / step response modes on top of the v0.1 foundation.

## Run

```powershell
py -3.14 -m venv .venv            # use a python.org Python (see note below)
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python main.py
```

Tests: `.venv\Scripts\python -m pytest`

> **Note (Anaconda):** a venv built on Anaconda's Python fails to import PySide6
> (`DLL load failed while importing QtCore`) because Anaconda ships an older MSVC
> runtime. Build the venv with a python.org interpreter instead.

## Features (v0.1)

**Input**
- Sketchable grid: draw directly on the input matrix (left-drag = brush value,
  right-drag = erase, double-click = type an exact value); resize, clear, randomise,
  or load a pattern.
- Image upload: converted to a grayscale pixel-intensity matrix (0–255) at a chosen
  resolution (16–256 px on the longest side).
- Kernel presets: identity, box / Gaussian blur, sharpen, Laplacian, Sobel X/Y,
  Prewitt X/Y, emboss — each available at 3×3 … 9×9.
- Custom kernel editor: any size up to 9×9 (rectangular allowed), editable values,
  normalise / zero.

**Computation & visualization**
- Adjustable stride, kernel size and padding mode (valid, zero, reflect, replicate, circular).
- Step-by-step animation (play/pause, step, scrub, speed, steps-per-tick for big images)
  with the sliding window highlighted on the padded input.
- Side-by-side input ⊛ flipped kernel = output, plus the multiply-add breakdown of
  each output sample.
- Result map: heatmap / grayscale rendering of input and output with colormap,
  scaling mode and colorbar.

Keyboard: `Space` play/pause · `←`/`→` step · `Home` reset · `End` finish.

## Features (v0.2)

**Reflect-and-shift & correlation comparison**
- Mode dropdown in the Computation card: switch between true **convolution** (kernel
  flipped) and **cross-correlation** (no flip).
- The step-by-step view updates its labels, operator glyph (⊛ vs ⋆) and equation
  breakdown dynamically.
- Live readout of **max |conv − corr|** — zero for symmetric kernels, non-zero otherwise.

**Causality & BIBO stability analyzer** (new Analysis card)
- **Causality** test under raster-scan ordering: reports whether the kernel is causal
  and, if not, the minimum origin shift *(a, b)* to make it causal.
- **BIBO stability**: computes *S = ΣΣ|h|*, *B = max|x|*, the theoretical bound
  *|y| ≤ B·S*, and compares it against the actual output maximum.
- **DC gain & classification**: displays *G = ΣΣh* and classifies the kernel as
  *averaging* (G ≠ 0) or *differencing* (G ≈ 0).

**Impulse & step response mode**
- New **2D Impulse** and **2D Step** patterns in the sketch grid's Patterns menu.
- Convolving with the impulse demonstrates that *y = h* (kernel = impulse response).
- Convolving with the step shows the accumulated response.

## Layout

```
main.py                     entry point
playground/core/            pure numpy: convolution.py, kernels.py, image_io.py, analyzer.py
playground/state.py         PlaygroundState — shared state + signals
playground/ui/              Qt widgets (matrix_grid.py, analyzer_panel.py, …)
tests/                      pytest suite for the core (128 tests)
```

