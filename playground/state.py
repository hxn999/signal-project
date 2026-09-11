"""Application state: single source of truth shared by every panel."""

from __future__ import annotations

import numpy as np
from PySide6.QtCore import QObject, Signal

from .core.convolution import ConvolutionError, ConvResult, convolve2d
from .core.kernels import make_preset

CUSTOM = "Custom"


def default_sketch() -> np.ndarray:
    x = np.zeros((10, 10))
    x[2:8, 2:8] = 1.0
    x[4:6, 4:6] = 0.0
    return x


class PlaygroundState(QObject):
    """Holds input, kernel and parameters; recomputes the convolution on change.

    Animation cursor ``step``:
      -1            nothing computed yet (reset)
      0 .. N-1      step k active: outputs 0..k shown, window at k highlighted
      N             finished: full output shown, no highlight
    """

    inputChanged = Signal()
    kernelChanged = Signal()
    paramsChanged = Signal()
    resultChanged = Signal()
    stepChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.sketch = default_sketch()
        self.image: np.ndarray | None = None
        self.image_path: str | None = None
        self.source = "sketch"               # "sketch" | "image"
        self.kernel_name = "Laplacian"
        self.kernel_size = 3
        self.kernel = make_preset(self.kernel_name, self.kernel_size)
        self.stride = (1, 1)
        self.padding = "zero"
        self.flip = True                     # true convolution (correlation toggle comes later)
        self.result: ConvResult | None = None
        self.error = ""
        self.step = -1
        self._recompute()

    # ---- derived -----------------------------------------------------------
    @property
    def input(self) -> np.ndarray:
        if self.source == "image" and self.image is not None:
            return self.image
        return self.sketch

    @property
    def num_steps(self) -> int:
        return self.result.num_steps if self.result is not None else 0

    # ---- input -------------------------------------------------------------
    def set_sketch(self, matrix: np.ndarray) -> None:
        self.sketch = np.asarray(matrix, dtype=np.float64)
        self.source = "sketch"
        self.inputChanged.emit()
        self._recompute()

    def set_sketch_cell(self, r: int, c: int, value: float) -> None:
        if self.sketch[r, c] == value and self.source == "sketch":
            return
        sketch = self.sketch.copy()
        sketch[r, c] = value
        self.set_sketch(sketch)

    def set_image(self, matrix: np.ndarray, path: str | None = None) -> None:
        self.image = np.asarray(matrix, dtype=np.float64)
        self.image_path = path
        self.source = "image"
        self.inputChanged.emit()
        self._recompute()

    def set_source(self, source: str) -> None:
        if source == "image" and self.image is None:
            return
        if source != self.source:
            self.source = source
            self.inputChanged.emit()
            self._recompute()

    # ---- kernel ------------------------------------------------------------
    def set_preset(self, name: str, size: int | None = None) -> None:
        size = self.kernel_size if size is None else size
        self.kernel_name, self.kernel_size = name, size
        self.kernel = make_preset(name, size)
        self.kernelChanged.emit()
        self._recompute()

    def set_kernel(self, kernel: np.ndarray, name: str = CUSTOM) -> None:
        self.kernel = np.asarray(kernel, dtype=np.float64)
        self.kernel_name = name
        self.kernelChanged.emit()
        self._recompute()

    # ---- parameters --------------------------------------------------------
    def set_stride(self, sh: int, sw: int) -> None:
        if (sh, sw) != self.stride:
            self.stride = (sh, sw)
            self.paramsChanged.emit()
            self._recompute()

    def set_padding(self, padding: str) -> None:
        if padding != self.padding:
            self.padding = padding
            self.paramsChanged.emit()
            self._recompute()

    # ---- animation cursor ----------------------------------------------------
    def set_step(self, step: int) -> None:
        step = max(-1, min(int(step), self.num_steps))
        if step != self.step:
            self.step = step
            self.stepChanged.emit(step)

    def _recompute(self) -> None:
        try:
            self.result = convolve2d(self.input, self.kernel, self.stride, self.padding, self.flip)
            self.error = ""
        except ConvolutionError as exc:
            self.result = None
            self.error = str(exc)
        self.step = self.num_steps  # show the finished result; play restarts from 0
        self.resultChanged.emit()
        self.stepChanged.emit(self.step)
