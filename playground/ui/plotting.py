"""Matplotlib styling shared by the result map and the application pages."""

from __future__ import annotations

import numpy as np

from . import theme


def style_axes(ax, title: str, ticks: bool = True, fontsize: int = 11) -> None:
    ax.set_facecolor(theme.SURFACE)
    ax.set_title(title, color=theme.TEXT, fontsize=fontsize, pad=8, loc="left")
    ax.tick_params(colors=theme.TEXT_FAINT, labelsize=8, length=3)
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(theme.BORDER)


def colorbar(figure, im, ax) -> None:
    cb = figure.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cb.outline.set_edgecolor(theme.BORDER)
    cb.ax.tick_params(colors=theme.TEXT_FAINT, labelsize=8)


def show(ax, data: np.ndarray, title: str, cmap: str = "gray", vmin: float | None = 0.0,
         vmax: float | None = 255.0, figure=None):
    """imshow with the app styling; pass ``figure`` to add a colorbar."""
    if vmin is None or vmax is None:
        lo, hi = float(np.min(data)), float(np.max(data))
        vmin, vmax = (lo if vmin is None else vmin), (hi if vmax is None else vmax)
    if vmax <= vmin:
        vmax = vmin + 1.0
    im = ax.imshow(data, cmap=cmap, vmin=vmin, vmax=vmax, interpolation="nearest")
    style_axes(ax, title, ticks=False, fontsize=10)
    if figure is not None:
        colorbar(figure, im, ax)
    return im
