# 2D Convolution Playground — Documentation

An interactive desktop app (PySide6 / Qt 6 + NumPy) for **CSE 219 — Signals and Linear
Systems**. It treats a 2D kernel as the impulse response of a 2D LTI system, animates the
convolution one output sample at a time, analyses the system (causality, BIBO stability, DC
gain), and applies the same theory to seven image-processing applications that run on a
from-scratch FFT.

Every algorithm uses only concepts from the course syllabus (`syllabus.md`): signals and
energy, impulse/step, LTI systems and convolution, causality and stability, Fourier
series/transform, DTFT/DFT, FFT, DFT properties, and sampling/reconstruction. There is no
machine learning, no DCT, and no SciPy or OpenCV.

## Running

```powershell
py -3.14 -m venv .venv            # use a python.org Python, not Anaconda
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python main.py
```

Tests: `.venv\Scripts\python -m pytest` (201 tests, about 2 s).

Requirements: PySide6 ≥ 6.6, NumPy ≥ 1.26, Matplotlib ≥ 3.8, Pillow ≥ 10.

## The window

| Area | What it holds |
|---|---|
| **Sidebar** (left) | Input, Kernel, Computation and Analysis cards. Hidden on the Applications tab. |
| **Step-by-step** tab | Input ⊛ kernel = output, with the sliding window and the multiply-add breakdown. |
| **Result map** tab | Heatmap / grayscale rendering of the input and the output. |
| **Applications** tab | Seven sub-tabs, one per application. |
| **Status bar** | Input size and source, kernel, stride, padding, output size, or the current error. |

## Feature guide

| Page | Features |
|---|---|
| [Convolution playground](convolution-playground.md) | Sketch grid, image upload, kernel presets and editor, stride and padding, step-by-step animation, result map |
| [LTI system analysis](lti-analysis.md) | Convolution vs cross-correlation, causality, BIBO stability, DC gain, impulse and step response |
| [FFT engine](fft.md) | Radix-2, mixed-radix Cooley–Tukey, Bluestein, 2D DFT, fast convolution |
| [Applications: shared parts](applications/README.md) | Page layout, image sources, sample images, filter helpers |
| [Image compression](applications/compression.md) | Block 2D DFT with coefficient dropping or quantisation |
| [Object detection](applications/detection.md) | Template matching by normalised cross-correlation |
| [Portrait mode](applications/portrait.md) | Layered lens blur with three ways to find the subject |
| [Deconvolution](applications/deconvolution.md) | Regularised inverse filtering of a known blur |
| [Canny edge detection](applications/canny.md) | Five-stage edge detector |
| [Stereo vision](applications/stereo.md) | Disparity and depth by block matching |
| [Super resolution](applications/superres.md) | ZOH, linear and ideal (sinc) reconstruction, aliasing demo |
| [Architecture](architecture.md) | Code layout, state and signals, how to add a page, testing |

## Syllabus map

| Course topic | Where it appears |
|---|---|
| Impulse, unit step | Impulse / step patterns; box sums as "accumulate then difference" |
| LTI systems, convolution | Whole playground; every application |
| Reflect-and-shift, correlation | Conv/corr toggle; object detection |
| Causality, BIBO stability | Analysis card |
| Signal energy | Detection (normalisation), stereo (matching cost), compression (Parseval) |
| Rect ↔ sinc, modulation | Portrait (disc kernel), super resolution (ZOH ↔ sinc, triangle ↔ sinc²) |
| DFT / IDFT, bins, conjugate symmetry | FFT engine; compression storage count |
| Radix-2 DIT FFT, bit reversal | `fft.py` |
| Cooley–Tukey N = N₁N₂, Bailey's four-step | `fft.py` mixed-radix path, 2D DFT |
| Bluestein (chirp-z) | `fft.py`, prime lengths |
| Circular convolution, zero-padding to L+M−1 | Fast convolution; deconvolution padding |
| Parseval | Compression energy kept |
| Sampling theorem, aliasing | Super resolution |
| Ideal LPF / ZOH / linear-interpolation reconstruction | Super resolution |
