"""Heatmap / grayscale rendering of the input and convolved output (matplotlib)."""

from __future__ import annotations

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import QComboBox, QHBoxLayout, QVBoxLayout, QWidget

from ..state import PlaygroundState
from . import theme
from .matrix_grid import format_value
from .widgets import Card, label

COLORMAPS = {
    "Grayscale": "gray",
    "Heatmap (inferno)": "inferno",
    "Viridis": "viridis",
    "Magma": "magma",
    "Diverging (coolwarm)": "coolwarm",
}
NORMALIZATIONS = ("Min–max", "Clip to 0–255", "Absolute value |y|", "Symmetric ±max")


class ResultView(QWidget):
    def __init__(self, state: PlaygroundState, parent=None):
        super().__init__(parent)
        self.state = state
        self._dirty = True

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 12, 0, 0)
        root.setSpacing(12)

        controls = QHBoxLayout()
        controls.addWidget(label("Colormap", "dim"))
        self.cmap = QComboBox()
        for name, key in COLORMAPS.items():
            self.cmap.addItem(name, key)
        controls.addWidget(self.cmap)
        controls.addSpacing(16)
        controls.addWidget(label("Output scaling", "dim"))
        self.norm = QComboBox()
        self.norm.addItems(NORMALIZATIONS)
        controls.addWidget(self.norm)
        controls.addStretch(1)
        self.stats = label("", "dim")
        controls.addWidget(self.stats)
        for combo in (self.cmap, self.norm):
            combo.currentIndexChanged.connect(self._mark_dirty)
        root.addLayout(controls)

        card = Card()
        self.figure = Figure(facecolor=theme.SURFACE, layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setStyleSheet(f"background: {theme.SURFACE};")
        card.body.addWidget(self.canvas, 1)
        root.addWidget(card, 1)

        state.resultChanged.connect(self._mark_dirty)

    def _mark_dirty(self) -> None:
        self._dirty = True
        if self.isVisible():
            self.refresh()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        if self._dirty:
            self.refresh()

    def _style_axes(self, ax, title: str) -> None:
        ax.set_facecolor(theme.SURFACE)
        ax.set_title(title, color=theme.TEXT, fontsize=11, pad=10, loc="left")
        ax.tick_params(colors=theme.TEXT_FAINT, labelsize=8, length=3)
        for spine in ax.spines.values():
            spine.set_color(theme.BORDER)

    def _colorbar(self, im, ax) -> None:
        cb = self.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cb.outline.set_edgecolor(theme.BORDER)
        cb.ax.tick_params(colors=theme.TEXT_FAINT, labelsize=8)

    def refresh(self) -> None:
        self._dirty = False
        self.figure.clear()
        s, res = self.state, self.state.result
        x = s.input
        cmap = self.cmap.currentData()

        ax_in, ax_out = self.figure.subplots(1, 2)
        is_image = s.source == "image"
        vmin, vmax = (0, 255) if is_image else (float(x.min()), float(x.max()))
        im = ax_in.imshow(x, cmap="gray", vmin=vmin, vmax=vmax if vmax > vmin else vmin + 1,
                          interpolation="nearest")
        self._style_axes(ax_in, f"Input  x[m, n]  ({x.shape[0]}×{x.shape[1]})")
        self._colorbar(im, ax_in)

        if res is None:
            self._style_axes(ax_out, "Output")
            ax_out.text(0.5, 0.5, s.error, color=theme.ERROR, ha="center", va="center",
                        transform=ax_out.transAxes, wrap=True)
            ax_out.set_xticks([])
            ax_out.set_yticks([])
            self.stats.setText("")
        else:
            y = res.output
            data, lo, hi = self._scaled(y)
            im = ax_out.imshow(data, cmap=cmap, vmin=lo, vmax=hi, interpolation="nearest")
            self._style_axes(ax_out, f"Output  y[m, n] = (x ⊛ h)  ({y.shape[0]}×{y.shape[1]})")
            self._colorbar(im, ax_out)
            self.stats.setText(f"y: min {format_value(float(y.min()))}  ·  max {format_value(float(y.max()))}"
                               f"  ·  mean {format_value(float(y.mean()))}")
        self.canvas.draw_idle()

    def _scaled(self, y: np.ndarray) -> tuple[np.ndarray, float, float]:
        mode = self.norm.currentText()
        if mode.startswith("Clip"):
            return np.clip(y, 0, 255), 0.0, 255.0
        if mode.startswith("Absolute"):
            y = np.abs(y)
        if mode.startswith("Symmetric"):
            a = float(np.abs(y).max()) or 1.0
            return y, -a, a
        lo, hi = float(y.min()), float(y.max())
        return y, lo, hi if hi > lo else lo + 1.0
