"""Shared scaffolding for the application pages.

Each page = a control column (image source, parameters, results, explanation)
and a matplotlib figure. Parameter changes schedule a debounced recompute that
only runs while the page is visible.
"""

from __future__ import annotations

import os

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import QObject, Qt, QTimer, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from ...core.image_io import IMAGE_FILTER, load_image_matrix
from ...core.samples import SAMPLES
from ...state import PlaygroundState
from .. import theme
from ..widgets import Card, label

APP_RESOLUTIONS = (128, 256, 512)
PLAYGROUND = "Playground input"
FILE = "Image file"
CONTROL_WIDTH = 350


class AppContext(QObject):
    """Results shared between pages (the stereo depth map feeds portrait mode)."""

    stereoChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.stereo_left: np.ndarray | None = None
        self.stereo_disparity: np.ndarray | None = None

    def set_stereo(self, left: np.ndarray, disparity: np.ndarray) -> None:
        self.stereo_left, self.stereo_disparity = left, disparity
        self.stereoChanged.emit()


def load_matrix_dialog(parent: QWidget, title: str, max_side: int) -> tuple[np.ndarray, str] | None:
    path, _ = QFileDialog.getOpenFileName(parent, title, "", IMAGE_FILTER)
    if not path:
        return None
    try:
        return load_image_matrix(path, max_side), path
    except Exception as exc:  # unreadable / unsupported file
        QMessageBox.warning(parent, "Could not open image", f"{os.path.basename(path)}\n\n{exc}")
        return None


class ImageSource(QWidget):
    """Sample image / the playground's current input / an image file, at a chosen size."""

    changed = Signal()

    def __init__(self, state: PlaygroundState, default_sample: str, parent=None):
        super().__init__(parent)
        self.state = state
        self.path: str | None = None
        self._cache: tuple[tuple, np.ndarray] | None = None
        v = QVBoxLayout(self)
        v.setContentsMargins(0, 0, 0, 0)
        v.setSpacing(8)

        self.combo = QComboBox()
        for name in SAMPLES:
            self.combo.addItem(f"Sample · {name}", ("sample", name))
        self.combo.addItem(PLAYGROUND, ("playground", None))
        self.combo.addItem(FILE, ("file", None))
        self.combo.setCurrentIndex(list(SAMPLES).index(default_sample))
        v.addWidget(self.combo)

        row = QHBoxLayout()
        self.load_btn = QPushButton("Load image…")
        self.load_btn.clicked.connect(self._choose)
        row.addWidget(self.load_btn, 1)
        self.resolution = QComboBox()
        for r in APP_RESOLUTIONS:
            self.resolution.addItem(f"{r} px", r)
        self.resolution.setCurrentIndex(APP_RESOLUTIONS.index(256))
        row.addWidget(self.resolution)
        v.addLayout(row)
        self.info = label("", "hint")
        self.info.setWordWrap(True)
        v.addWidget(self.info)

        self.combo.currentIndexChanged.connect(self._on_combo)
        self.resolution.currentIndexChanged.connect(self.changed.emit)
        state.inputChanged.connect(self._on_playground_input)

    def _on_combo(self) -> None:
        if self.combo.currentData()[0] == "file" and self.path is None:
            self._choose()
            return
        self.changed.emit()

    def _on_playground_input(self) -> None:
        if self.combo.currentData()[0] == "playground":
            self.changed.emit()

    def _choose(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open image", "", IMAGE_FILTER)
        if not path:
            if self.path is None and self.combo.currentData()[0] == "file":
                self.combo.setCurrentIndex(0)
            return
        self.path = path
        self._cache = None
        self.combo.blockSignals(True)
        self.combo.setCurrentIndex(self.combo.count() - 1)
        self.combo.blockSignals(False)
        self.changed.emit()

    @property
    def is_sample(self) -> str | None:
        kind, name = self.combo.currentData()
        return name if kind == "sample" else None

    def image(self) -> np.ndarray:
        kind, name = self.combo.currentData()
        size = self.resolution.currentData()
        if kind == "playground":
            x = self.state.input.astype(float)
            if self.state.source == "sketch":       # sketch values are small numbers
                lo, hi = float(x.min()), float(x.max())
                x = (x - lo) * (255.0 / (hi - lo)) if hi > lo else np.zeros_like(x)
            self.info.setText(f"Playground {self.state.source} · {x.shape[0]}×{x.shape[1]}")
            return x
        key = (kind, name, size, self.path)
        if self._cache is None or self._cache[0] != key:
            if kind == "sample":
                x = SAMPLES[name](size)
            else:
                try:
                    x = load_image_matrix(self.path, size)
                except Exception as exc:
                    raise ValueError(f"could not read {self.path}: {exc}") from exc
            self._cache = (key, x)
        x = self._cache[1]
        where = os.path.basename(self.path) if kind == "file" else name
        self.info.setText(f"{where} · {x.shape[0]}×{x.shape[1]}")
        return x


class AppPage(QWidget):
    TITLE = ""
    CONCEPT = ""            # rich-text explanation of the syllabus ideas used
    DEFAULT_SAMPLE = "Shapes"

    def __init__(self, state: PlaygroundState, context: AppContext, parent=None):
        super().__init__(parent)
        self.state = state
        self.context = context
        self._dirty = True

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 12, 0, 0)
        root.setSpacing(12)

        controls = QWidget()
        cv = QVBoxLayout(controls)
        cv.setContentsMargins(0, 0, 6, 0)
        cv.setSpacing(12)

        self.source_card = Card("Image")
        self.source = ImageSource(state, self.DEFAULT_SAMPLE)
        self.source.changed.connect(self._on_source_changed)
        self.source_card.body.addWidget(self.source)
        cv.addWidget(self.source_card)

        params = Card("Parameters")
        self.form = QFormLayout()
        self.form.setHorizontalSpacing(10)
        self.form.setVerticalSpacing(8)
        self.form.setLabelAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        params.body.addLayout(self.form)
        cv.addWidget(params)

        results = Card("Results")
        self.stats = label("", "dim")
        self.stats.setWordWrap(True)
        self.stats.setTextFormat(Qt.RichText)
        results.body.addWidget(self.stats)
        cv.addWidget(results)

        concept = Card("How it works")
        text = label(self.CONCEPT, "hint")
        text.setWordWrap(True)
        text.setTextFormat(Qt.RichText)
        concept.body.addWidget(text)
        cv.addWidget(concept)
        cv.addStretch(1)

        scroll = QScrollArea()
        scroll.setWidget(controls)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setFixedWidth(CONTROL_WIDTH)
        root.addWidget(scroll)

        card = Card()
        self.figure = Figure(facecolor=theme.SURFACE, layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setStyleSheet(f"background: {theme.SURFACE};")
        card.body.addWidget(self.canvas, 1)
        root.addWidget(card, 1)

        self._timer = QTimer(self, singleShot=True, interval=250)
        self._timer.timeout.connect(self.refresh)

        self.build_controls()

    # ---- hooks -----------------------------------------------------------------
    def build_controls(self) -> None:
        """Add widgets to ``self.form``."""

    def compute(self) -> None:
        """Run the algorithm and draw on ``self.figure`` (already cleared)."""
        raise NotImplementedError

    def on_source_changed(self) -> None:
        """Called when the image changes, before the recompute."""

    # ---- form helpers -------------------------------------------------------------
    def add_row(self, text: str, widget: QWidget) -> QWidget:
        self.form.addRow(label(text, "dim"), widget)
        return widget

    def add_spin(self, text: str, lo: int, hi: int, value: int, step: int = 1,
                 suffix: str = "") -> QSpinBox:
        spin = QSpinBox(singleStep=step, suffix=suffix)
        spin.setRange(lo, hi)
        spin.setValue(value)
        spin.valueChanged.connect(self.schedule)
        return self.add_row(text, spin)

    def add_dspin(self, text: str, lo: float, hi: float, value: float, step: float,
                  decimals: int = 2, suffix: str = "") -> QDoubleSpinBox:
        spin = QDoubleSpinBox(singleStep=step, suffix=suffix)
        spin.setDecimals(decimals)   # before the value, or it is rounded to 2 decimals
        spin.setRange(lo, hi)
        spin.setValue(value)
        spin.valueChanged.connect(self.schedule)
        return self.add_row(text, spin)

    def add_combo(self, text: str, items) -> QComboBox:
        combo = QComboBox()
        for item in items:
            if isinstance(item, tuple):
                combo.addItem(item[0], item[1])
            else:
                combo.addItem(str(item), item)
        combo.currentIndexChanged.connect(self.schedule)
        return self.add_row(text, combo)

    def add_check(self, text: str, checked: bool = False) -> QCheckBox:
        box = QCheckBox(text)
        box.setChecked(checked)
        box.toggled.connect(self.schedule)
        self.form.addRow(box)
        return box

    def set_row_visible(self, widget: QWidget, visible: bool) -> None:
        self.form.setRowVisible(widget, visible)

    # ---- recompute ------------------------------------------------------------------
    def _on_source_changed(self) -> None:
        self.on_source_changed()
        self.schedule()

    def schedule(self) -> None:
        self._dirty = True
        if self.isVisible():
            self._timer.start()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if self._dirty:
            self._timer.start(0)

    def refresh(self) -> None:
        if not self.isVisible():
            return
        self._dirty = False
        self.figure.clear()
        QGuiApplication.setOverrideCursor(Qt.WaitCursor)
        try:
            self.compute()
        except Exception as exc:  # show the problem instead of crashing the app
            self.figure.clear()
            ax = self.figure.add_subplot(1, 1, 1)
            ax.set_axis_off()
            ax.text(0.5, 0.5, f"⚠ {exc}", color=theme.ERROR, ha="center", va="center",
                    transform=ax.transAxes, wrap=True)
            self.stats.setText("")
        finally:
            QGuiApplication.restoreOverrideCursor()
        self.canvas.draw_idle()

    def set_stats(self, rows: list[tuple[str, str]]) -> None:
        self.stats.setText("<table cellspacing='0' cellpadding='2'>" + "".join(
            f"<tr><td style='color:{theme.TEXT_DIM}; padding-right:10px'>{k}</td>"
            f"<td style='color:{theme.TEXT}'>{v}</td></tr>" for k, v in rows) + "</table>")
