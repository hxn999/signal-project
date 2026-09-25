"""Stereo vision: depth from the horizontal shift between two views.

A point at depth Z appears in the right camera shifted left by the
disparity d = f·B / Z pixels (f focal length, B baseline). For every
candidate d the right image is shifted by d (a pure time shift,
x[n - d]) and compared with the left image through the energy of the
difference, summed over a block with a box filter:

    C_d[m, n] = sum_block (L[m, n] - R[m, n - d])²

The disparity of each pixel is the d that minimises C_d; depth follows as
Z = f·B / d.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .filters import box_sum


@dataclass(frozen=True)
class StereoResult:
    disparity: np.ndarray    # pixels
    cost: np.ndarray         # best matching cost per pixel
    depth: np.ndarray        # f·B / d (arbitrary units)


def shift_right(x: np.ndarray, d: int) -> np.ndarray:
    """y[m, n] = x[m, n - d], edge-replicated where n - d < 0."""
    if d == 0:
        return x.copy()
    y = np.empty_like(x)
    y[:, d:] = x[:, :-d]
    y[:, :d] = x[:, :1]
    return y


def disparity_map(left: np.ndarray, right: np.ndarray, max_disp: int = 16, block: int = 7,
                  focal_baseline: float = 100.0) -> StereoResult:
    left = np.asarray(left, dtype=float)
    right = np.asarray(right, dtype=float)
    if left.shape != right.shape:
        raise ValueError("left and right images must have the same size")
    max_disp = max(0, min(int(max_disp), left.shape[1] - 1))
    best = np.full(left.shape, np.inf)
    disp = np.zeros(left.shape)
    for d in range(max_disp + 1):
        diff = left - shift_right(right, d)
        cost = box_sum(diff * diff, block, block, "same")
        better = cost < best
        best[better] = cost[better]
        disp[better] = d
    depth = focal_baseline / np.maximum(disp, 0.5)
    return StereoResult(disp, best, depth)


def default_disparity_layers(shape: tuple[int, int], max_disp: int = 12) -> np.ndarray:
    """A far background, a mid-distance rectangle and a near disc (true disparities)."""
    h, w = shape
    d = np.full(shape, max(1, max_disp // 6), dtype=float)
    d[h // 5:h * 4 // 5, w // 10:w * 2 // 5] = max_disp // 2
    rr, cc = np.mgrid[0:h, 0:w]
    near = (rr - h * 0.55) ** 2 + (cc - w * 0.68) ** 2 <= (min(h, w) * 0.2) ** 2
    d[near] = max_disp
    return d


def synthetic_pair(img: np.ndarray, disparity: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Render a right view from ``img`` (the left view) and a disparity map.

    Each left pixel (m, n) lands at (m, n - d). Pixels are painted far to near so
    nearer surfaces occlude farther ones; uncovered holes take the background shift.
    """
    left = np.asarray(img, dtype=float)
    w = left.shape[1]
    d = np.round(disparity).astype(int)
    right = np.empty_like(left)
    bg = int(d.min())
    right[:, :w - bg] = left[:, bg:]
    right[:, w - bg:] = left[:, -1:]
    for level in np.unique(d):
        rows, cols = np.nonzero(d == level)
        target = cols - level
        ok = target >= 0
        right[rows[ok], target[ok]] = left[rows[ok], cols[ok]]
    return left, right
