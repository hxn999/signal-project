"""Image compression page: block 2D DFT, drop / quantise coefficients, rebuild."""

from __future__ import annotations

import numpy as np

from ...core.compression import METHODS, compress
from ..plotting import show
from .base import AppPage


class CompressionPage(AppPage):
    TITLE = "Compression"
    DEFAULT_SAMPLE = "Shapes"
    CONCEPT = (
        "Each B×B block goes through a <b>2D DFT</b> (rows, then columns). Natural images "
        "keep most of their energy in a few low-frequency bins, so the rest can be "
        "discarded (JPEG's idea).<br><br>"
        "<b>Keep largest</b>: store only the top K % of bins by |X[k]|.<br>"
        "<b>Quantise</b>: round X[k]/q to integers, with q growing with frequency, "
        "so fine detail is stored coarsely and most bins round to 0.<br><br>"
        "<b>Conjugate symmetry</b> X[−k] = X[k]* of a real block means a kept pair costs "
        "2 real numbers and DC / Nyquist cost 1: the stored-number count equals the kept-bin "
        "count. <b>Parseval</b> turns 'spectral energy kept' into 'signal energy kept'.")

    def build_controls(self) -> None:
        self.method = self.add_combo("Method", METHODS)
        self.block = self.add_combo("Block size", [("8 × 8", 8), ("16 × 16", 16), ("32 × 32", 32),
                                                   ("64 × 64", 64), ("Whole image", 0)])
        self.keep = self.add_dspin("Keep", 0.1, 100.0, 10.0, 1.0, 1, " %")
        self.step = self.add_dspin("Quantiser step", 1.0, 500.0, 20.0, 5.0, 1)
        self.method.currentIndexChanged.connect(self._sync_rows)
        self._sync_rows()

    def _sync_rows(self) -> None:
        topk = self.method.currentIndex() == 0
        self.set_row_visible(self.keep, topk)
        self.set_row_visible(self.step, not topk)

    def compute(self) -> None:
        x = self.source.image()
        res = compress(x, self.block.currentData() or None, self.method.currentText(),
                       self.keep.value() / 100.0, self.step.value())
        axs = self.figure.subplots(2, 2)
        show(axs[0, 0], x, f"Original  ({x.shape[0]}×{x.shape[1]})")
        show(axs[0, 1], np.clip(res.reconstruction, 0, 255),
             f"Reconstruction  (ratio {res.ratio:.1f} : 1)")
        err = np.abs(x - res.reconstruction)
        show(axs[1, 0], err, "Error |x − x̂|", cmap="magma", vmin=0, vmax=None, figure=self.figure)
        bh, bw = res.block
        show(axs[1, 1], res.kept_map, f"Kept bins per {bh}×{bw} block (centred, DC in middle)",
             cmap="viridis", vmin=0, vmax=1)
        psnr = "∞ (lossless)" if res.psnr == float("inf") else f"{res.psnr:.2f} dB"
        self.set_stats([
            ("Pixels", f"{res.total:,}"),
            ("Stored numbers", f"{res.kept:,}"),
            ("Compression", f"{res.ratio:.2f} : 1"),
            ("Energy kept", f"{100 * res.energy_kept:.3f} %"),
            ("MSE", f"{res.mse:.2f}"),
            ("PSNR", psnr),
        ])
