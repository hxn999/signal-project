"""Canny edge detector assembled from convolutions.

1. Smooth: x ⊛ Gaussian (a low-pass LTI system — derivatives amplify noise).
2. Gradient: Sobel X / Sobel Y kernels (differencing systems, DC gain 0).
3. Magnitude sqrt(gx² + gy²) and direction atan2(gy, gx), rounded to 0/45/90/135°.
4. Non-maximum suppression: keep a pixel only if it beats both neighbours
   across the edge, which thins edges to one pixel.
5. Double threshold + hysteresis: strong pixels are edges; weak pixels
   survive only if they connect (8-neighbourhood) to a strong one.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .convolution import convolve2d
from .filters import filter2d, gaussian
from .kernels import sobel_x, sobel_y

# direction bin -> (dr, dc) offset of one neighbour across the edge
_NEIGHBOUR = {0: (0, 1), 1: (1, 1), 2: (1, 0), 3: (1, -1)}


@dataclass(frozen=True)
class CannyResult:
    smoothed: np.ndarray
    gx: np.ndarray
    gy: np.ndarray
    magnitude: np.ndarray    # normalised to max 1
    direction: np.ndarray    # degrees in [0, 180)
    suppressed: np.ndarray   # after non-maximum suppression
    strong: np.ndarray
    weak: np.ndarray
    edges: np.ndarray


def _shift(a: np.ndarray, dr: int, dc: int) -> np.ndarray:
    """out[r, c] = a[r + dr, c + dc] (zero outside)."""
    h, w = a.shape
    out = np.zeros_like(a)
    out[max(0, -dr):h - max(0, dr), max(0, -dc):w - max(0, dc)] = \
        a[max(0, dr):h - max(0, -dr), max(0, dc):w - max(0, -dc)]
    return out


def non_max_suppression(mag: np.ndarray, direction: np.ndarray) -> np.ndarray:
    bins = (np.round(direction / 45.0).astype(int)) % 4
    out = np.zeros_like(mag)
    for b, (dr, dc) in _NEIGHBOUR.items():
        sel = bins == b
        # strict on one side: of two equal pixels straddling an edge only one survives
        keep = sel & (mag > _shift(mag, dr, dc)) & (mag >= _shift(mag, -dr, -dc))
        out[keep] = mag[keep]
    return out


def hysteresis(strong: np.ndarray, weak: np.ndarray) -> np.ndarray:
    edges = strong.copy()
    candidates = strong | weak
    while True:
        grown = edges.copy()
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    grown |= _shift(edges, dr, dc)
        grown &= candidates
        if np.array_equal(grown, edges):
            return edges
        edges = grown


def canny(img: np.ndarray, sigma: float = 1.4, low: float = 0.1, high: float = 0.25) -> CannyResult:
    """low / high are fractions of the largest gradient magnitude."""
    x = np.asarray(img, dtype=float)
    smoothed = filter2d(x, gaussian(sigma)) if sigma > 0 else x.copy()
    gx = convolve2d(smoothed, sobel_x(3), padding="replicate").output
    gy = convolve2d(smoothed, sobel_y(3), padding="replicate").output
    mag = np.hypot(gx, gy)
    peak = float(mag.max())
    mag = mag / peak if peak > 0 else mag
    direction = np.degrees(np.arctan2(gy, gx)) % 180.0
    nms = non_max_suppression(mag, direction)
    strong = nms >= high
    weak = (nms >= low) & ~strong
    return CannyResult(smoothed, gx, gy, mag, direction, nms, strong, weak,
                       hysteresis(strong, weak))
