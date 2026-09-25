"""Super resolution page: sampling-theory reconstruction (ZOH, linear, ideal sinc)."""

from __future__ import annotations

import numpy as np

from ...core.fft import log_spectrum
from ...core.filters import psnr
from ...core.superres import METHODS, crop_to_multiple, downsample, unsharp, upsample
from ..plotting import show
from .base import AppPage


class SuperResPage(AppPage):
    TITLE = "Super resolution"
    DEFAULT_SAMPLE = "Zone plate"
    CONCEPT = (
        "Upscaling ×f = reconstructing the continuous image from its samples and "
        "re-sampling f times finer. All three methods insert f − 1 zeros between samples "
        "(spectrum copies appear) and then <b>low-pass filter</b> them away:<br>"
        "• <b>Zero-order hold</b>: h₀ = rect → H₀ ~ sinc, leaks copies (blocky).<br>"
        "• <b>Linear</b>: h₁ = h₀ ⊛ h₀ (triangle) → H₁ ~ sinc², less leakage.<br>"
        "• <b>Ideal</b>: brick-wall LPF with cutoff π/f = sinc interpolation, done exactly by "
        "<b>zero-padding the DFT</b>.<br><br>"
        "<b>Simulate</b> mode first downsamples the image. Without the anti-alias "
        "LPF, frequencies above the new <b>Nyquist</b> limit fold back (aliasing) and no "
        "reconstruction can undo it — try the zone plate. An optional unsharp mask "
        "x + a(x − x ⊛ g) re-boosts attenuated high frequencies.")

    def build_controls(self) -> None:
        self.mode = self.add_combo("Mode", [("Simulate: downsample, then upscale", "simulate"),
                                            ("Upscale the image itself", "upscale")])
        self.factor = self.add_spin("Factor f", 2, 8, 2, 1, " ×")
        self.antialias = self.add_check("Anti-alias LPF before downsampling", True)
        self.sharpen = self.add_dspin("Unsharp amount", 0.0, 3.0, 0.0, 0.25, 2)
        self.mode.currentIndexChanged.connect(
            lambda: self.set_row_visible(self.antialias, self.mode.currentData() == "simulate"))

    def compute(self) -> None:
        f = self.factor.value()
        simulate = self.mode.currentData() == "simulate"
        img = self.source.image()
        if simulate:
            ref = crop_to_multiple(img, f)
            low = downsample(ref, f, self.antialias.isChecked())
        else:
            if max(img.shape) * f > 1024:
                raise ValueError("result would exceed 1024 px — lower the factor or the resolution")
            ref, low = None, img
        if min(low.shape) < 4:
            raise ValueError("the low-resolution image is too small")

        ups = {m: np.clip(unsharp(upsample(low, f, m), self.sharpen.value()), 0, 255)
               for m in METHODS}

        axs = self.figure.subplots(2, 4)
        if simulate:
            show(axs[0, 0], ref, f"Original  ({ref.shape[0]}×{ref.shape[1]})")
            aa = "anti-aliased" if self.antialias.isChecked() else "aliased!"
            show(axs[1, 0], low, f"Samples ↓{f}  ({low.shape[0]}×{low.shape[1]}, {aa})")
        else:
            show(axs[0, 0], low, f"Input  ({low.shape[0]}×{low.shape[1]})")
            show(axs[1, 0], log_spectrum(low), "Input spectrum log|X|", cmap="inferno",
                 vmin=None, vmax=None)
        rows = [("Low-res", f"{low.shape[0]}×{low.shape[1]}"),
                ("Upscaled", f"{low.shape[0] * f}×{low.shape[1] * f}")]
        for i, (m, y) in enumerate(ups.items(), start=1):
            title = m
            if ref is not None:
                score = psnr(ref, y)
                title += f"  ·  {score:.1f} dB"
                rows.append((f"PSNR {m}", f"{score:.2f} dB"))
            show(axs[0, i], y, title)
            show(axs[1, i], log_spectrum(y), "spectrum log|Y|", cmap="inferno", vmin=None, vmax=None)
        self.set_stats(rows)
