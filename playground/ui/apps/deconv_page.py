"""Deconvolution page: blur an image with a known PSF, then invert it in the DFT domain."""

from __future__ import annotations

import numpy as np

from ...core.deconvolution import PSF_KINDS, degrade, inverse_filter, make_psf
from ...core.filters import psnr
from ..plotting import show
from .base import AppPage

SIZE_LABEL = {"Gaussian": "σ", "Motion": "length", "Defocus (disc)": "radius", "Box": "width"}
DEFAULT_SIZE = {"Gaussian": 2.0, "Motion": 12.0, "Defocus (disc)": 3.0, "Box": 5.0}


class DeconvPage(AppPage):
    TITLE = "Deconvolution"
    DEFAULT_SAMPLE = "Textured scene"
    CONCEPT = (
        "Blur is an LTI system: y = x ⊛ h. The <b>convolution theorem</b> gives "
        "Y[k] = X[k]·H[k], so the sharp image comes back by <b>dividing spectra</b>: "
        "X̂ = Y / H (inverse filter).<br><br>"
        "Where |H| ≈ 0 the blur erased that frequency, and dividing by it blows up noise. "
        "<b>ε</b> zeroes those bins; <b>K</b> writes 1/H = H*/|H|² and adds K to the "
        "denominator, capping the gain. K = ε = 0 is the pure inverse — try it with noise.<br><br>"
        "Multiplying DFTs is <b>circular</b> convolution: the image is mirror-padded first so "
        "the wrap does not pull the opposite edge in. Tick <i>circular blur</i> and untick "
        "padding to see the exact, wrap-consistent inverse.")

    def build_controls(self) -> None:
        self.mode = self.add_combo("Input", [("Sharp image → blur it here", "synthetic"),
                                             ("Already blurry → restore", "real")])
        self.kind = self.add_combo("Blur PSF h", PSF_KINDS)
        self.size = self.add_dspin("Size", 0.5, 40.0, 2.0, 0.5, 1)
        self.angle = self.add_dspin("Angle", 0.0, 180.0, 30.0, 15.0, 0, "°")
        self.noise = self.add_dspin("Noise σ", 0.0, 30.0, 0.5, 0.5, 2)
        self.circular = self.add_check("Circular blur (periodic image)", False)
        self.eps = self.add_dspin("ε  (cut |H| below)", 0.0, 0.5, 0.0, 0.005, 4)
        self.k = self.add_dspin("K  (regularise)", 0.0, 1.0, 0.002, 0.001, 4)
        self.pad = self.add_check("Mirror-pad before the DFT", True)
        self.kind.currentIndexChanged.connect(
            lambda: self.size.setValue(DEFAULT_SIZE[self.kind.currentText()]))
        self.kind.currentIndexChanged.connect(self._sync_rows)
        self.mode.currentIndexChanged.connect(self._sync_rows)
        self._sync_rows()

    def _sync_rows(self) -> None:
        kind = self.kind.currentText()
        self.form.labelForField(self.size).setText(f"Size ({SIZE_LABEL[kind]})")
        self.set_row_visible(self.angle, kind == "Motion")
        synthetic = self.mode.currentData() == "synthetic"
        for w in (self.noise, self.circular):
            self.set_row_visible(w, synthetic)

    def compute(self) -> None:
        x = self.source.image()
        psf = make_psf(self.kind.currentText(), self.size.value(), self.angle.value())
        if psf.shape[0] >= min(x.shape) // 2:
            raise ValueError("the blur kernel is too large for this image")
        synthetic = self.mode.currentData() == "synthetic"
        y = degrade(x, psf, self.noise.value(), self.circular.isChecked()) if synthetic else x
        res = inverse_filter(y, psf, self.eps.value(), self.k.value(), self.pad.isChecked())

        axs = self.figure.subplots(2, 3)
        show(axs[0, 0], x, "Original x" if synthetic else "Blurry input y")
        show(axs[0, 1], np.clip(y, 0, 255), "Blurred y = x ⊛ h (+ noise)" if synthetic else "Input y")
        show(axs[0, 2], np.clip(res.restored, 0, 255), "Restored x̂ = IDFT{Y·G}")
        show(axs[1, 0], psf, f"PSF h  ({psf.shape[0]}×{psf.shape[1]})", cmap="inferno",
             vmin=0, vmax=None)
        show(axs[1, 1], np.log10(res.otf_mag + 1e-6), "log₁₀|H[k]|  (blur response)",
             cmap="viridis", vmin=-4, vmax=0, figure=self.figure)
        show(axs[1, 2], np.log10(res.gain_mag + 1e-6), "log₁₀|G[k]|  (restoration gain)",
             cmap="magma", vmin=None, vmax=None, figure=self.figure)

        rows = [("PSF", f"{self.kind.currentText()} {psf.shape[0]}×{psf.shape[1]}"),
                ("Bins cut by ε", f"{100 * res.zeroed:.1f} %"),
                ("min |H|", f"{float(res.otf_mag.min()):.2e}"),
                ("max gain |G|", f"{float(res.gain_mag.max()):.1f}")]
        if synthetic:
            rows += [("PSNR blurred", f"{psnr(x, y):.2f} dB"),
                     ("PSNR restored", f"{psnr(x, np.clip(res.restored, 0, 255)):.2f} dB")]
        self.set_stats(rows)
