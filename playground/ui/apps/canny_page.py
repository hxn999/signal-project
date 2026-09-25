"""Canny edge detection page: every stage of the pipeline side by side."""

from __future__ import annotations

import numpy as np

from ...core.edges import canny
from ..plotting import show
from .base import AppPage


class CannyPage(AppPage):
    TITLE = "Canny edges"
    DEFAULT_SAMPLE = "Shapes"
    CONCEPT = (
        "<b>1. Smooth</b> with a Gaussian (low-pass LTI system): derivatives amplify "
        "high-frequency noise.<br>"
        "<b>2. Differentiate</b> with Sobel X / Y — differencing kernels with DC gain ΣΣh = 0.<br>"
        "<b>3.</b> |∇| = √(gx² + gy²), direction θ = atan2(gy, gx), rounded to 0/45/90/135°.<br>"
        "<b>4. Non-maximum suppression</b>: keep a pixel only if it beats both neighbours "
        "along θ — edges become 1 px thin.<br>"
        "<b>5. Hysteresis</b>: pixels above <i>high</i> are edges; pixels above <i>low</i> "
        "are kept only if connected to one.")

    def build_controls(self) -> None:
        self.sigma = self.add_dspin("Gaussian σ", 0.0, 6.0, 1.4, 0.2, 1)
        self.low = self.add_dspin("Low threshold", 1.0, 99.0, 8.0, 1.0, 1, " %")
        self.high = self.add_dspin("High threshold", 1.0, 100.0, 20.0, 1.0, 1, " %")

    def compute(self) -> None:
        x = self.source.image()
        low, high = sorted((self.low.value() / 100, self.high.value() / 100))
        res = canny(x, self.sigma.value(), low, high)
        axs = self.figure.subplots(2, 3)
        show(axs[0, 0], res.smoothed, f"1 · Smoothed (σ = {self.sigma.value():g})")
        show(axs[0, 1], res.magnitude, "2–3 · Gradient magnitude |∇|", cmap="inferno", vmin=0, vmax=1)
        hue = np.ma.masked_where(res.magnitude < 0.05, res.direction)
        show(axs[0, 2], hue, "3 · Direction θ (hue)", cmap="hsv", vmin=0, vmax=180)
        axs[0, 2].set_facecolor("black")
        show(axs[1, 0], res.suppressed, "4 · After non-max suppression", cmap="inferno", vmin=0, vmax=1)
        th = np.zeros(x.shape)
        th[res.weak] = 0.45
        th[res.strong] = 1.0
        show(axs[1, 1], th, "5 · Strong (white) / weak (grey)", vmin=0, vmax=1)
        show(axs[1, 2], res.edges.astype(float), "5 · Edges after hysteresis", vmin=0, vmax=1)
        n_edges = int(res.edges.sum())
        self.set_stats([
            ("Strong pixels", f"{int(res.strong.sum()):,}"),
            ("Weak pixels", f"{int(res.weak.sum()):,}"),
            ("Weak kept", f"{n_edges - int(res.strong.sum()):,}"),
            ("Edge pixels", f"{n_edges:,}  ({100 * n_edges / x.size:.1f} %)"),
            ("Thresholds", f"{100 * low:g} % / {100 * high:g} % of max |∇|"),
        ])
