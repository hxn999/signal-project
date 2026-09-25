"""Object detection by template matching (a matched filter).

Correlating the image with a template is convolving it with the template's
reflection, so it is an LTI system whose impulse response is the flipped
template — computed here with FFT fast convolution. Raw correlation favours
bright regions, so each score is normalised by the energies of the template
and of the image patch under it:

    ncc[m, n] = sum (x - x̄)(t - t̄) / sqrt( E_patch · E_template )   ∈ [-1, 1]

and equals 1 only where the patch is a scaled / offset copy of the template.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .fft import fast_correlate2d
from .filters import box_sum


@dataclass(frozen=True)
class Match:
    row: int        # top-left of the matched window
    col: int
    height: int
    width: int
    score: float


def ncc_map(image: np.ndarray, template: np.ndarray, eps: float = 1e-9) -> np.ndarray:
    """Normalised cross-correlation for every placement of the template inside the image."""
    x = np.asarray(image, dtype=float)
    t = np.asarray(template, dtype=float)
    th, tw = t.shape
    if th > x.shape[0] or tw > x.shape[1]:
        raise ValueError("template is larger than the image")
    t0 = t - t.mean()                       # zero mean -> sum t0 = 0
    e_t = float((t0 * t0).sum())
    num = fast_correlate2d(x, t0, "valid")  # = sum (x - x̄) t0 because sum t0 = 0
    n = th * tw
    s1 = box_sum(x, th, tw)
    s2 = box_sum(x * x, th, tw)
    e_patch = np.maximum(s2 - s1 * s1 / n, 0.0)   # energy of each zero-mean patch
    den = np.sqrt(e_patch * e_t)
    out = np.zeros_like(num)
    ok = den > eps * max(1.0, float(den.max(initial=0.0)))
    out[ok] = num[ok] / den[ok]
    return np.clip(out, -1.0, 1.0)


def find_matches(score: np.ndarray, template_shape: tuple[int, int], threshold: float = 0.8,
                 max_hits: int = 10) -> list[Match]:
    """Greedy peak picking: take the best score, suppress a template-sized area, repeat."""
    th, tw = template_shape
    s = score.copy()
    hits: list[Match] = []
    while len(hits) < max_hits:
        idx = int(np.argmax(s))
        r, c = divmod(idx, s.shape[1])
        best = float(s[r, c])
        if not best >= threshold:
            break
        hits.append(Match(r, c, th, tw, best))
        s[max(0, r - th // 2 - 1):r + th // 2 + 2, max(0, c - tw // 2 - 1):c + tw // 2 + 2] = -np.inf
    return hits
