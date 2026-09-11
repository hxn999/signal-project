"""Kernel controls: preset library, size and custom value editor."""

from __future__ import annotations

import numpy as np
from PySide6.QtWidgets import (
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ..core.kernels import PRESETS
from ..state import CUSTOM, PlaygroundState
from .matrix_grid import MatrixGrid, format_value
from .widgets import label

MAX_KERNEL = 9


def resize_centered(k: np.ndarray, rows: int, cols: int) -> np.ndarray:
    """Grow/shrink around the centre so the kernel origin stays put."""
    new = np.zeros((rows, cols))
    r, c = min(rows, k.shape[0]), min(cols, k.shape[1])
    sr, sc = (k.shape[0] - r) // 2, (k.shape[1] - c) // 2
    dr, dc = (rows - r) // 2, (cols - c) // 2
    new[dr:dr + r, dc:dc + c] = k[sr:sr + r, sc:sc + c]
    return new


class KernelPanel(QWidget):
    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)

        g = QGridLayout()
        g.setHorizontalSpacing(8)
        g.setVerticalSpacing(8)
        self.preset = QComboBox()
        last_category = None
        for name, (category, _) in PRESETS.items():
            if last_category is not None and category != last_category:
                self.preset.insertSeparator(self.preset.count())
            self.preset.addItem(f"{name}", name)
            self.preset.setItemData(self.preset.count() - 1, category, 3)  # tooltip role
            last_category = category
        self.preset.insertSeparator(self.preset.count())
        self.preset.addItem("Custom", CUSTOM)
        self.preset.currentIndexChanged.connect(self._on_preset)
        g.addWidget(label("Preset", "dim"), 0, 0)
        g.addWidget(self.preset, 0, 1)

        self.rows = QSpinBox(minimum=1, maximum=MAX_KERNEL)
        self.cols = QSpinBox(minimum=1, maximum=MAX_KERNEL)
        self.rows.valueChanged.connect(self._on_size)
        self.cols.valueChanged.connect(self._on_size)
        size_row = QHBoxLayout()
        size_row.addWidget(self.rows, 1)
        size_row.addWidget(label("×", "dim"))
        size_row.addWidget(self.cols, 1)
        g.addWidget(label("Kernel size", "dim"), 1, 0)
        g.addLayout(size_row, 1, 1)
        g.setColumnStretch(1, 1)
        v.addLayout(g)

        self.grid = MatrixGrid(editable=True, max_cell=46, symbol="h")
        self.grid.cmap = "diverging"
        self.grid.setFixedHeight(210)
        self.grid.cellEdited.connect(self._on_cell)
        v.addWidget(self.grid)

        info_row = QHBoxLayout()
        self.info = label("", "dim")
        info_row.addWidget(self.info, 1)
        normalize = QPushButton("Normalize")
        normalize.setToolTip("Divide by ΣΣh so the kernel has unit DC gain")
        normalize.clicked.connect(self._normalize)
        zero = QPushButton("Zero")
        zero.clicked.connect(lambda: self.state.set_kernel(np.zeros_like(self.state.kernel)))
        info_row.addWidget(normalize)
        info_row.addWidget(zero)
        v.addLayout(info_row)

        hint = label("Double-click a value to edit it (Enter jumps to the next cell). "
                     "Editing a preset turns it into a custom kernel.", "hint")
        hint.setWordWrap(True)
        v.addWidget(hint)

        state.kernelChanged.connect(self._sync)
        self._sync()

    @property
    def _is_preset(self) -> bool:
        return self.state.kernel_name in PRESETS

    def _on_preset(self) -> None:
        name = self.preset.currentData()
        if name == CUSTOM:
            self.state.set_kernel(self.state.kernel, CUSTOM)
            return
        n = max(self.state.kernel.shape)
        n = max(3, n if n % 2 else n + 1)
        self.state.set_preset(name, min(n, MAX_KERNEL))

    def _on_size(self, value: int) -> None:
        if self._is_preset:
            old = self.state.kernel_size
            if value % 2 == 0:  # presets are odd-sized: step in the direction of change
                value = value + 1 if value > old else value - 1
            value = max(3, min(value, MAX_KERNEL))
            self.state.set_preset(self.state.kernel_name, value)
        else:
            self.state.set_kernel(resize_centered(self.state.kernel, self.rows.value(), self.cols.value()))

    def _on_cell(self, r: int, c: int, value: float) -> None:
        k = self.state.kernel.copy()
        k[r, c] = value
        self.state.set_kernel(k, CUSTOM)

    def _normalize(self) -> None:
        s = self.state.kernel.sum()
        if abs(s) > 1e-12 and abs(s - 1) > 1e-12:
            self.state.set_kernel(self.state.kernel / s, CUSTOM)

    def _sync(self) -> None:
        k = self.state.kernel
        widgets = (self.preset, self.rows, self.cols)
        for w in widgets:
            w.blockSignals(True)
        self.preset.setCurrentIndex(self.preset.findData(self.state.kernel_name))
        preset = self._is_preset
        for spin, value in ((self.rows, k.shape[0]), (self.cols, k.shape[1])):
            spin.setMinimum(3 if preset else 1)
            spin.setSingleStep(2 if preset else 1)
            spin.setValue(value)
        for w in widgets:
            w.blockSignals(False)
        self.grid.set_matrix(k)
        self.info.setText(f"ΣΣh = {format_value(float(k.sum()))}")
