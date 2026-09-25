"""Object detection page: template matching with normalised cross-correlation."""

from __future__ import annotations

import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.widgets import RectangleSelector
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from ...core.detection import find_matches, ncc_map
from ...core.samples import pattern_positions, pattern_template
from .. import theme
from ..plotting import show
from .base import AppPage, load_matrix_dialog


class DetectionPage(AppPage):
    TITLE = "Object detection"
    DEFAULT_SAMPLE = "Repeated objects"
    CONCEPT = (
        "A <b>matched filter</b>: correlating the image with the template t is convolving "
        "it with t reflected, h[m, n] = t[−m, −n] — an LTI system whose output peaks where "
        "the image looks like t. It is computed as a <b>fast convolution</b> "
        "(zero-pad to L + M − 1, FFT, multiply, IFFT).<br><br>"
        "Raw correlation prefers bright areas, so each score is divided by the "
        "<b>energies</b> of the template and of the patch (both made zero-mean): "
        "ncc = Σ(x − x̄)(t − t̄) / √(E<sub>x</sub>·E<sub>t</sub>) ∈ [−1, 1], "
        "= 1 for a perfect (brightness / contrast-shifted) copy. "
        "Local patch energies come from box sums — accumulate (⊛ unit step), then difference.<br><br>"
        "<b>Drag a rectangle</b> on the image to choose the template.")

    def build_controls(self) -> None:
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        load = QPushButton("Load template…")
        load.clicked.connect(self._load_template)
        reset = QPushButton("Reset")
        reset.clicked.connect(self._reset_template)
        h.addWidget(load, 1)
        h.addWidget(reset)
        self.add_row("Template", row)
        self.threshold = self.add_dspin("Threshold", 0.1, 1.0, 0.8, 0.05, 2)
        self.max_hits = self.add_spin("Max matches", 1, 50, 10)
        self.noise = self.add_dspin("Add noise σ", 0.0, 80.0, 0.0, 5.0, 1)
        self.rect: tuple[int, int, int, int] | None = None     # r0, c0, r1, c1 (exclusive)
        self.loaded: np.ndarray | None = None
        self._selector = None

    def on_source_changed(self) -> None:
        self.rect = None

    def _reset_template(self) -> None:
        self.rect, self.loaded = None, None
        self.schedule()

    def _load_template(self) -> None:
        got = load_matrix_dialog(self, "Open template", 128)
        if got is not None:
            self.loaded = got[0]
            self.schedule()

    def _default_rect(self, shape: tuple[int, int]) -> tuple[int, int, int, int]:
        h, w = shape
        if self.source.is_sample == "Repeated objects":
            n = pattern_template(max(h, w)).shape[0]
            r, c = pattern_positions(max(h, w))[0]
            return r, c, r + n, c + n
        s = max(8, min(h, w) // 8)
        return h // 2 - s // 2, w // 2 - s // 2, h // 2 + s - s // 2, w // 2 + s - s // 2

    def _on_select(self, press, release) -> None:
        r0, r1 = sorted((int(round(press.ydata)), int(round(release.ydata))))
        c0, c1 = sorted((int(round(press.xdata)), int(round(release.xdata))))
        if r1 - r0 >= 3 and c1 - c0 >= 3:
            self.rect, self.loaded = (r0, c0, r1 + 1, c1 + 1), None
            self.schedule()

    def compute(self) -> None:
        clean = self.source.image()
        x = clean
        if self.noise.value() > 0:
            x = clean + np.random.default_rng(7).normal(0, self.noise.value(), clean.shape)
        if self.loaded is not None:
            template = self.loaded
            if template.shape[0] > x.shape[0] or template.shape[1] > x.shape[1]:
                raise ValueError("the template is larger than the image")
        else:
            if self.rect is None or self.rect[2] > x.shape[0] or self.rect[3] > x.shape[1]:
                self.rect = self._default_rect(x.shape)
            r0, c0, r1, c1 = self.rect
            template = clean[r0:r1, c0:c1]

        score = ncc_map(x, template)
        hits = find_matches(score, template.shape, self.threshold.value(), self.max_hits.value())

        gs = self.figure.add_gridspec(2, 2, width_ratios=(2.2, 1))
        ax_img = self.figure.add_subplot(gs[:, 0])
        ax_t = self.figure.add_subplot(gs[0, 1])
        ax_s = self.figure.add_subplot(gs[1, 1])
        show(ax_img, x, f"Image — {len(hits)} match{'es' if len(hits) != 1 else ''}")
        if self.loaded is None:
            r0, c0, r1, c1 = self.rect
            ax_img.add_patch(Rectangle((c0 - 0.5, r0 - 0.5), c1 - c0, r1 - r0, fill=False,
                                       ec=theme.ACCENT, lw=1.2, ls="--"))
        for m in hits:
            ax_img.add_patch(Rectangle((m.col - 0.5, m.row - 0.5), m.width, m.height, fill=False,
                                       ec=theme.HIGHLIGHT, lw=1.8))
            ax_img.text(m.col, m.row - 2, f"{m.score:.2f}", color=theme.HIGHLIGHT, fontsize=8,
                        va="bottom")
        show(ax_t, template, f"Template t  ({template.shape[0]}×{template.shape[1]})")
        show(ax_s, score, "Normalised correlation", cmap="coolwarm", vmin=-1, vmax=1,
             figure=self.figure)
        for m in hits:
            ax_s.plot(m.col, m.row, "o", mfc="none", mec=theme.HIGHLIGHT, ms=7)

        self._selector = RectangleSelector(ax_img, self._on_select, useblit=True, button=[1],
                                           minspanx=3, minspany=3, interactive=False,
                                           props=dict(ec=theme.ACCENT, fc=theme.ACCENT, alpha=0.2))
        rows = [("Template", f"{template.shape[0]}×{template.shape[1]}"),
                ("Score map", f"{score.shape[0]}×{score.shape[1]}"),
                ("Matches", str(len(hits)))]
        rows += [(f"#{i + 1}", f"({m.row}, {m.col})  ncc {m.score:.3f}") for i, m in enumerate(hits[:8])]
        self.set_stats(rows)
