"""Input controls: sketchable grid settings and image upload."""

from __future__ import annotations

import os

import numpy as np
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QGridLayout,
    QHBoxLayout,
    QMenu,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ..core.image_io import IMAGE_FILTER, RESOLUTIONS, load_image_matrix
from ..state import PlaygroundState
from .widgets import label

MAX_SKETCH = 64


def _pattern(name: str, rows: int, cols: int, value: float) -> np.ndarray:
    x = np.zeros((rows, cols))
    r0, c0 = rows // 4, cols // 4
    r1, c1 = rows - r0, cols - c0
    if name == "Square":
        x[r0:r1, c0:c1] = value
    elif name == "Ring":
        x[r0:r1, c0:c1] = value
        x[r0 + 1:r1 - 1, c0 + 1:c1 - 1] = 0
    elif name == "Cross":
        x[rows // 2, :] = value
        x[:, cols // 2] = value
    elif name == "Diagonal":
        for i in range(min(rows, cols)):
            x[i, i] = value
    elif name == "Checkerboard":
        i, j = np.indices((rows, cols))
        x[(i + j) % 2 == 0] = value
    elif name == "Vertical edge":
        x[:, cols // 2:] = value
    elif name == "Gradient":
        x[:] = np.linspace(0, value, cols)[None, :]
    return x


def _resized(old: np.ndarray, rows: int, cols: int) -> np.ndarray:
    new = np.zeros((rows, cols))
    r, c = min(rows, old.shape[0]), min(cols, old.shape[1])
    new[:r, :c] = old[:r, :c]
    return new


class InputPanel(QWidget):
    brushChanged = Signal(float)
    imageLoaded = Signal()

    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        self._rng = np.random.default_rng()

        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(0)

        # segmented control; only the active page is shown so the card fits it
        seg = QHBoxLayout()
        seg.setSpacing(0)
        self.source_group = QButtonGroup(self)
        for i, text in enumerate(("Sketch grid", "Image")):
            b = QPushButton(text, checkable=True)
            b.setObjectName("segLeft" if i == 0 else "segRight")
            self.source_group.addButton(b, i)
            seg.addWidget(b, 1)
        lay.addLayout(seg)
        self.pages = [self._build_sketch_tab(), self._build_image_tab()]
        for page in self.pages:
            lay.addWidget(page)
        self.source_group.idClicked.connect(self._on_tab)

        state.inputChanged.connect(self._sync)
        self._sync()

    # ---- sketch --------------------------------------------------------------
    def _build_sketch_tab(self) -> QWidget:
        w = QWidget()
        g = QGridLayout(w)
        g.setContentsMargins(0, 10, 0, 0)
        g.setHorizontalSpacing(8)
        g.setVerticalSpacing(8)

        self.rows = QSpinBox(minimum=2, maximum=MAX_SKETCH)
        self.cols = QSpinBox(minimum=2, maximum=MAX_SKETCH)
        self.rows.valueChanged.connect(self._on_resize)
        self.cols.valueChanged.connect(self._on_resize)
        size_row = QHBoxLayout()
        size_row.addWidget(self.rows, 1)
        size_row.addWidget(label("×", "dim"))
        size_row.addWidget(self.cols, 1)
        g.addWidget(label("Size", "dim"), 0, 0)
        g.addLayout(size_row, 0, 1)

        self.brush = QDoubleSpinBox(minimum=-999, maximum=999, decimals=2, value=1.0, singleStep=1.0)
        self.brush.valueChanged.connect(self.brushChanged)
        g.addWidget(label("Brush value", "dim"), 1, 0)
        g.addWidget(self.brush, 1, 1)

        buttons = QHBoxLayout()
        clear = QPushButton("Clear")
        clear.clicked.connect(lambda: self.state.set_sketch(np.zeros_like(self.state.sketch)))
        rand = QPushButton("Random")
        rand.clicked.connect(self._random)
        patterns = QToolButton(text="Patterns ▾")
        patterns.setPopupMode(QToolButton.InstantPopup)
        menu = QMenu(patterns)
        for name in ("Square", "Ring", "Cross", "Diagonal", "Checkerboard", "Vertical edge", "Gradient"):
            menu.addAction(name, lambda n=name: self._apply_pattern(n))
        patterns.setMenu(menu)
        for b in (clear, rand, patterns):
            buttons.addWidget(b)
        g.addLayout(buttons, 2, 0, 1, 2)

        hint = label("Draw directly on the input grid: left-drag paints the brush value, "
                     "right-drag erases, double-click types an exact value.", "hint")
        hint.setWordWrap(True)
        g.addWidget(hint, 3, 0, 1, 2)
        g.setColumnStretch(1, 1)
        return w

    def _on_resize(self) -> None:
        rows, cols = self.rows.value(), self.cols.value()
        if (rows, cols) != self.state.sketch.shape:
            self.state.set_sketch(_resized(self.state.sketch, rows, cols))

    def _random(self) -> None:
        self.state.set_sketch(self._rng.integers(0, 10, size=self.state.sketch.shape).astype(float))

    def _apply_pattern(self, name: str) -> None:
        rows, cols = self.state.sketch.shape
        self.state.set_sketch(_pattern(name, rows, cols, self.brush.value() or 1.0))

    # ---- image ---------------------------------------------------------------
    def _build_image_tab(self) -> QWidget:
        w = QWidget()
        v = QVBoxLayout(w)
        v.setContentsMargins(0, 10, 0, 0)
        v.setSpacing(8)

        upload = QPushButton("Upload image…")
        upload.setObjectName("primary")
        upload.clicked.connect(self._choose_image)
        v.addWidget(upload)

        row = QHBoxLayout()
        row.addWidget(label("Resolution (longest side)", "dim"))
        self.resolution = QComboBox()
        for r in RESOLUTIONS:
            self.resolution.addItem(f"{r} px", r)
        self.resolution.setCurrentIndex(RESOLUTIONS.index(32))
        self.resolution.currentIndexChanged.connect(self._reload_image)
        row.addWidget(self.resolution)
        v.addLayout(row)

        self.preview = label("No image loaded", "hint")
        self.preview.setAlignment(Qt.AlignCenter)
        self.preview.setMinimumHeight(150)
        self.preview.setStyleSheet("border: 1px dashed #2a2f3a; border-radius: 8px;")
        v.addWidget(self.preview)
        self.image_info = label("", "hint")
        self.image_info.setWordWrap(True)
        v.addWidget(self.image_info)
        hint = label("The image is converted to a grayscale pixel-intensity matrix (0–255). "
                     "Small resolutions keep the step-by-step view readable.", "hint")
        hint.setWordWrap(True)
        v.addWidget(hint)
        return w

    def _choose_image(self) -> None:
        start = os.path.dirname(self.state.image_path) if self.state.image_path else ""
        path, _ = QFileDialog.getOpenFileName(self, "Open image", start, IMAGE_FILTER)
        if path:
            self.load_image(path)

    def load_image(self, path: str) -> bool:
        try:
            matrix = load_image_matrix(path, self.resolution.currentData())
        except Exception as exc:  # unreadable / unsupported file
            QMessageBox.warning(self, "Could not open image", f"{os.path.basename(path)}\n\n{exc}")
            return False
        self.state.set_image(matrix, path)
        self.imageLoaded.emit()
        return True

    def _reload_image(self) -> None:
        if self.state.image_path:
            try:
                matrix = load_image_matrix(self.state.image_path, self.resolution.currentData())
            except OSError:
                return
            self.state.set_image(matrix, self.state.image_path)

    def _update_preview(self) -> None:
        img = self.state.image
        if img is None:
            return
        data = np.ascontiguousarray(np.clip(img, 0, 255).astype(np.uint8))
        h, w = data.shape
        qimg = QImage(data.data, w, h, w, QImage.Format_Grayscale8).copy()
        pm = QPixmap.fromImage(qimg).scaled(self.preview.width() - 8, 150, Qt.KeepAspectRatio,
                                            Qt.FastTransformation)
        self.preview.setPixmap(pm)
        name = os.path.basename(self.state.image_path or "image")
        self.image_info.setText(f"{name} → {h}×{w} matrix")

    # ---- sync -----------------------------------------------------------------
    def _show_page(self, index: int) -> None:
        self.source_group.button(index).setChecked(True)
        for i, page in enumerate(self.pages):
            page.setVisible(i == index)

    def _on_tab(self, index: int) -> None:
        self._show_page(index)
        self.state.set_source("image" if index == 1 else "sketch")

    def _sync(self) -> None:
        for spin, value in ((self.rows, self.state.sketch.shape[0]), (self.cols, self.state.sketch.shape[1])):
            spin.blockSignals(True)
            spin.setValue(value)
            spin.blockSignals(False)
        self._show_page(1 if self.state.source == "image" else 0)
        self._update_preview()
