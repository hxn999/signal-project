"""Portrait mode page: lens blur behind a chosen subject."""

from __future__ import annotations

import numpy as np
from matplotlib.patches import Ellipse

from ...core.portrait import (
    amount_from_disparity,
    amount_from_mask,
    ellipse_mask,
    lens_blur,
    sharpness_map,
)
from .. import theme
from ..plotting import show
from .base import AppPage

ELLIPSE, SHARPNESS, STEREO = "ellipse", "sharpness", "stereo"


class PortraitPage(AppPage):
    TITLE = "Portrait mode"
    DEFAULT_SAMPLE = "Shapes"
    CONCEPT = (
        "An out-of-focus lens spreads every point into a disc, so defocus is "
        "<b>convolution with a pillbox</b> h = disc(r) — a 2D rect in the radius, whose "
        "spectrum is sinc-like ripples (the 'bokeh' look). Its radius grows with distance "
        "from the focal plane.<br><br>"
        "The image is split into blur layers; each is convolved (FFT fast convolution) with "
        "its own disc and the layers are blended. <b>Normalised convolution</b> "
        "(x·m ⊛ h) / (m ⊛ h) keeps the sharp subject from bleeding into the background.<br><br>"
        "Where is the subject?<br>"
        "• <b>Ellipse</b>: click the subject.<br>"
        "• <b>Sharpness</b>: local energy of the Laplacian (high frequencies) is large only "
        "where the photo is already in focus.<br>"
        "• <b>Stereo depth</b>: blur ∝ |d − d<sub>focus</sub>| from the Stereo tab; click "
        "to choose the focus distance.<br>"
        "Masks are feathered by a Gaussian convolution.")

    def build_controls(self) -> None:
        self.mask_src = self.add_combo("Subject from", [("Ellipse (click subject)", ELLIPSE),
                                                        ("Sharpness map (auto)", SHARPNESS),
                                                        ("Stereo depth (click focus)", STEREO)])
        self.ell_h = self.add_spin("Ellipse height", 5, 100, 55, 5, " %")
        self.ell_w = self.add_spin("Ellipse width", 5, 100, 40, 5, " %")
        self.window = self.add_spin("Sharpness window", 3, 61, 15, 2, " px")
        self.thresh = self.add_dspin("Sharpness threshold", 0.01, 1.0, 0.15, 0.01, 2)
        self.feather_s = self.add_dspin("Feather σ", 0.0, 20.0, 4.0, 0.5, 1)
        self.radius = self.add_dspin("Max blur radius", 1.0, 30.0, 8.0, 1.0, 1, " px")
        self.layers = self.add_spin("Blur layers", 2, 10, 5)
        self.click: tuple[float, float] | None = None
        self._ax_click = None
        self.canvas.mpl_connect("button_press_event", self._on_click)
        self.mask_src.currentIndexChanged.connect(self._sync_rows)
        self.context.stereoChanged.connect(self._on_stereo)
        self._sync_rows()

    def _sync_rows(self) -> None:
        src = self.mask_src.currentData()
        for w in (self.ell_h, self.ell_w):
            self.set_row_visible(w, src == ELLIPSE)
        for w in (self.window, self.thresh):
            self.set_row_visible(w, src == SHARPNESS)
        self.source_card.setVisible(src != STEREO)
        self.click = None

    def _on_stereo(self) -> None:
        if self.mask_src.currentData() == STEREO:
            self.schedule()

    def on_source_changed(self) -> None:
        self.click = None

    def _on_click(self, event) -> None:
        if event.inaxes is self._ax_click and event.button == 1 and event.xdata is not None:
            self.click = (event.ydata, event.xdata)
            self.schedule()

    def compute(self) -> None:
        src = self.mask_src.currentData()
        feather = self.feather_s.value()
        if src == STEREO:
            if self.context.stereo_left is None:
                raise ValueError("run the Stereo vision tab first — its depth map is used here")
            x, disp = self.context.stereo_left, self.context.stereo_disparity
            h, w = x.shape
            r, c = self.click or (h * 0.55, w * 0.68)
            r, c = int(np.clip(r, 0, h - 1)), int(np.clip(c, 0, w - 1))
            focus = float(np.median(disp[max(0, r - 2):r + 3, max(0, c - 2):c + 3]))
            amount = amount_from_disparity(disp, focus, feather_sigma=feather)
            info = ("Focus disparity", f"{focus:g} px at ({r}, {c})")
        else:
            x = self.source.image()
            h, w = x.shape
            if src == ELLIPSE:
                center = self.click or (h / 2, w / 2)
                axes = (h * self.ell_h.value() / 200, w * self.ell_w.value() / 200)
                mask = ellipse_mask(x.shape, center, axes)
                info = ("Subject centre", f"({center[0]:.0f}, {center[1]:.0f})")
            else:
                sharp = sharpness_map(x, self.window.value())
                mask = (sharp >= self.thresh.value()).astype(float)
                info = ("Sharp area", f"{100 * mask.mean():.1f} % of pixels")
            amount = amount_from_mask(mask, feather)

        out = lens_blur(x, amount, self.radius.value(), self.layers.value())
        axs = self.figure.subplots(1, 3)
        show(axs[0], x, "Original  (click to focus)" if src != SHARPNESS else "Original")
        self._ax_click = axs[0]
        if src == ELLIPSE:
            axs[0].add_patch(Ellipse((center[1], center[0]), 2 * axes[1], 2 * axes[0], fill=False,
                                     ec=theme.HIGHLIGHT, lw=1.4, ls="--"))
        elif src == STEREO:
            axs[0].plot(c, r, "+", color=theme.HIGHLIGHT, ms=14, mew=2)
        show(axs[1], amount, "Blur amount (0 = in focus)", cmap="magma", vmin=0, vmax=1,
             figure=self.figure)
        show(axs[2], np.clip(out, 0, 255), f"Lens blur (r ≤ {self.radius.value():g} px)")
        self.set_stats([info,
                        ("In focus", f"{100 * np.mean(amount < 0.05):.1f} % of pixels"),
                        ("Disc radii", ", ".join(f"{self.radius.value() * i / (self.layers.value() - 1):.1f}"
                                                 for i in range(self.layers.value())))])
