# Architecture

## Layout

```
main.py                       entry point: QApplication + theme + MainWindow
playground/
  state.py                    PlaygroundState: single source of truth + Qt signals
  core/                       pure NumPy, no Qt imports; everything here is unit-tested
    convolution.py            convolve2d, padding, ConvResult / Step replay
    kernels.py                preset kernel library
    analyzer.py               causality, BIBO, DC gain, conv/corr difference
    image_io.py               image file -> grayscale 0–255 matrix
    fft.py                    from-scratch FFT, 2D DFT, fast convolution
    filters.py                Gaussian / disc / motion / triangle kernels, filter2d, box_sum, PSNR
    samples.py                synthetic test images
    compression.py  detection.py  portrait.py  deconvolution.py
    edges.py  stereo.py  superres.py          one module per application
  ui/
    main_window.py            sidebar + tabs + status bar + keyboard shortcuts
    theme.py                  colour tokens and the Qt stylesheet (dark theme)
    widgets.py                Card, label(), painted transport icons
    plotting.py               shared Matplotlib styling (style_axes, colorbar, show)
    matrix_grid.py            QPainter matrix view / editor / sketch canvas
    input_panel.py  kernel_panel.py  compute_panel.py  analyzer_panel.py   sidebar cards
    step_view.py  animation_bar.py  result_view.py                         playground tabs
    apps/
      base.py                 AppPage, ImageSource, AppContext, form helpers
      applications_view.py    the Applications tab (a QTabWidget of pages)
      *_page.py               one page per application
tests/                        pytest: test_convolution, test_kernels, test_analyzer,
                              test_fft, test_applications
```

**Rule:** `core/` never imports Qt. The UI calls the core, never the other way round. The
math can therefore be tested and reused without a display.

## State and signals (playground)

`PlaygroundState` (a `QObject`) owns the sketch, the image, the kernel, stride, padding, flip
and the animation step. Panels call its setters (`set_sketch`, `set_image`, `set_preset`,
`set_kernel`, `set_stride`, `set_padding`, `set_flip`, `set_step`, …). Every input or
parameter change runs `_recompute()`, which:

1. calls `convolve2d` for the current mode and for the opposite flip (for the conv/corr
   difference),
2. stores any `ConvolutionError` message in `state.error`,
3. sets the step to "finished" and emits the signals.

| Signal | Emitted when | Main listeners |
|---|---|---|
| `inputChanged` | Sketch, image or source changes | InputPanel, AnimationBar, ImageSource ("Playground input") |
| `kernelChanged` | Preset or custom kernel changes | KernelPanel, AnalyzerPanel |
| `paramsChanged` | Stride, padding or flip changes | |
| `resultChanged` | After every recompute | StepView, ResultView, ComputePanel, AnalyzerPanel, AnimationBar, status bar |
| `stepChanged(int)` | The animation cursor moves | StepView, AnimationBar |
| `flipChanged(bool)` | The mode toggles | StepView |

`ResultView` and the application pages redraw lazily: they mark themselves dirty and only
draw when visible.

## Application pages

`AppPage` (in `ui/apps/base.py`) provides the page layout, the `ImageSource`, a debounced
(250 ms), visibility-aware `refresh()` with a busy cursor and on-figure error display, and
form helpers.

`AppContext` carries results between pages. It currently holds the stereo left image and
disparity map, and emits `stereoChanged` for Portrait mode.

### Adding a new application

1. Put the algorithm in `playground/core/<name>.py` as pure NumPy functions. Reuse
   `fft.fast_convolve2d`, `filters.filter2d` and `filters.box_sum` rather than writing new
   convolution code.
2. Add tests to `tests/test_applications.py`.
3. Create `playground/ui/apps/<name>_page.py`:

   ```python
   class MyPage(AppPage):
       TITLE = "My app"
       DEFAULT_SAMPLE = "Shapes"          # a key of core.samples.SAMPLES
       CONCEPT = "Rich-text explanation of the syllabus ideas used."

       def build_controls(self):
           self.sigma = self.add_dspin("σ", 0.0, 5.0, 1.0, 0.1, 1)
           self.mode = self.add_combo("Mode", ["A", "B"])

       def compute(self):                 # the figure is already cleared
           x = self.source.image()
           y = my_algorithm(x, self.sigma.value())
           a, b = self.figure.subplots(1, 2)
           show(a, x, "Input")
           show(b, y, "Output")
           self.set_stats([("Metric", "value")])
   ```

   Helpers: `add_spin`, `add_dspin`, `add_combo` (strings or `(label, data)` tuples),
   `add_check`, `add_row` (any widget), `set_row_visible`, `schedule()`, and the
   `on_source_changed()` hook. Every helper already connects its widget to `schedule`.
4. Add the class to `PAGES` in `applications_view.py`.

`QDoubleSpinBox` pitfall: set the decimals *before* the value, or the value is rounded to
2 decimals. `add_dspin` already does this.

## Styling

`theme.py` defines the colour tokens (`BG`, `SURFACE`, `TEXT`, `ACCENT`, `HIGHLIGHT`,
`NEGATIVE`, `POSITIVE`, `ERROR`, …) and one Qt stylesheet. Widgets opt in through object
names:

- `card`, `cardTitle`, `dim`, `hint`, `error` for text and containers
- `primary` for buttons
- `segLeft` / `segRight` for the segmented control
- `transport` / `play` for the animation buttons

Matplotlib figures use `plotting.show` / `style_axes` / `colorbar` so they match the Qt
surface colour.

## Testing

```powershell
.venv\Scripts\python -m pytest            # 201 tests
```

| File | Covers |
|---|---|
| `test_convolution.py` | `convolve2d` against a double-loop reference for every padding mode and stride; shapes; errors |
| `test_kernels.py` | Preset shapes, DC gains and validation; image → intensity conversion |
| `test_analyzer.py` | Causality shift, BIBO bound, DC gain, symmetry |
| `test_fft.py` | FFT against `numpy.fft` for power-of-2, mixed-radix and prime N; Parseval; conjugate symmetry; shift property; lecture examples; fast convolution against `convolve2d` |
| `test_applications.py` | Filters, samples, and every application (lossless compression, planted templates found, exact inverse filtering, thin Canny edges, recovered disparity, untouched in-focus pixels, exact sinc upsampling, aliasing) |

UI code has no automated tests. To smoke-test it without a display, set
`QT_QPA_PLATFORM=offscreen`, build `MainWindow`, and call `refresh()` on each page.
