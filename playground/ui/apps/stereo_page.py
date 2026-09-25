"""Stereo vision page: disparity / depth by block matching two views."""

from __future__ import annotations

import os

import numpy as np
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QWidget

from ...core.stereo import default_disparity_layers, disparity_map, synthetic_pair
from ..plotting import show
from .base import AppPage, load_matrix_dialog


class StereoPage(AppPage):
    TITLE = "Stereo vision"
    DEFAULT_SAMPLE = "Textured scene"
    CONCEPT = (
        "Two cameras a baseline B apart see a point at depth Z shifted horizontally by the "
        "<b>disparity</b> d = f·B / Z — near objects shift more.<br><br>"
        "For every candidate d the right view is <b>time-shifted</b>, R[m, n − d], and "
        "compared with the left view by the <b>energy</b> of the difference, summed over a "
        "block with a <b>box filter</b> (accumulate with a unit step, then difference):<br>"
        "C<sub>d</sub> = Σ<sub>block</sub> (L − R<sub>d</sub>)².<br>"
        "Each pixel takes the d with the lowest cost; depth is Z = f·B / d.<br><br>"
        "No stereo camera? <i>Synthetic pair</i> renders a right view from any image with "
        "three depth layers, and shows the true disparity. The result also drives the "
        "<b>Portrait</b> tab's depth mode.")

    def build_controls(self) -> None:
        self.mode = self.add_combo("Stereo pair", [("Synthetic pair from image", "synthetic"),
                                                   ("Load left + right images", "files")])
        row = QWidget()
        h = QHBoxLayout(row)
        h.setContentsMargins(0, 0, 0, 0)
        self.left_btn = QPushButton("Left…")
        self.right_btn = QPushButton("Right…")
        self.left_btn.clicked.connect(lambda: self._load(0))
        self.right_btn.clicked.connect(lambda: self._load(1))
        h.addWidget(self.left_btn)
        h.addWidget(self.right_btn)
        self.load_row = self.add_row("Files", row)
        self.true_disp = self.add_spin("Scene disparity (near)", 2, 40, 12, 1, " px")
        self.max_disp = self.add_spin("Search range", 1, 64, 16, 1, " px")
        self.block = self.add_spin("Block size", 3, 31, 9, 2, " px")
        self.fb = self.add_dspin("f·B", 1.0, 10000.0, 100.0, 10.0, 0)
        self.pair: list[np.ndarray | None] = [None, None]
        self.names = ["", ""]
        self.mode.currentIndexChanged.connect(self._sync_rows)
        self._sync_rows()

    def _sync_rows(self) -> None:
        files = self.mode.currentData() == "files"
        self.set_row_visible(self.load_row, files)
        self.set_row_visible(self.true_disp, not files)
        self.source_card.setVisible(not files)

    def _load(self, which: int) -> None:
        got = load_matrix_dialog(self, "Open left image" if which == 0 else "Open right image",
                                 self.source.resolution.currentData())
        if got is not None:
            self.pair[which] = got[0]
            self.names[which] = os.path.basename(got[1])
            self.schedule()

    def compute(self) -> None:
        truth = None
        if self.mode.currentData() == "files":
            left, right = self.pair
            if left is None or right is None:
                raise ValueError("load both a left and a right image")
            if left.shape != right.shape:
                raise ValueError(f"left {left.shape} and right {right.shape} sizes differ")
        else:
            truth = default_disparity_layers(self.source.image().shape, self.true_disp.value())
            left, right = synthetic_pair(self.source.image(), truth)

        res = disparity_map(left, right, self.max_disp.value(), self.block.value(), self.fb.value())
        self.context.set_stereo(left, res.disparity)

        axs = self.figure.subplots(2, 3)
        show(axs[0, 0], left, "Left view L")
        show(axs[0, 1], right, "Right view R")
        show(axs[0, 2], np.abs(left - right), "|L − R|  (shift is visible)", cmap="magma",
             vmin=0, vmax=None)
        dmax = max(self.max_disp.value(), 1)
        show(axs[1, 0], res.disparity, "Estimated disparity d (px)", cmap="viridis", vmin=0,
             vmax=dmax, figure=self.figure)
        if truth is not None:
            show(axs[1, 1], truth, "True disparity", cmap="viridis", vmin=0, vmax=dmax,
                 figure=self.figure)
        else:
            show(axs[1, 1], np.sqrt(res.cost), "Matching cost √C (lower = surer)", cmap="magma",
                 vmin=0, vmax=None, figure=self.figure)
        depth = np.minimum(res.depth, np.percentile(res.depth, 98))
        show(axs[1, 2], depth, "Depth Z = f·B / d", cmap="magma_r", vmin=None, vmax=None,
             figure=self.figure)

        rows = [("Image", f"{left.shape[0]}×{left.shape[1]}"),
                ("Disparities tried", f"0 … {self.max_disp.value()}"),
                ("Block", f"{self.block.value()}×{self.block.value()}")]
        if truth is not None:
            b = self.block.value()
            inner = (slice(b, -b), slice(b + dmax, -b))
            err = np.abs(res.disparity - truth)[inner]
            rows += [("Exact", f"{100 * np.mean(err == 0):.1f} %"),
                     ("Within 1 px", f"{100 * np.mean(err <= 1):.1f} %"),
                     ("", "(interior, away from borders)")]
        else:
            rows += [("Files", f"{self.names[0]} / {self.names[1]}")]
        self.set_stats(rows)
