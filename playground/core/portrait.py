"""Portrait mode: synthetic shallow depth of field (lens blur).

An out-of-focus lens spreads each point into a disc, so defocus is
convolution with a pillbox h = disc(r) whose radius grows with distance
from the focal plane. The image is split into blur layers; every layer is
blurred with its own disc and the layers are blended back.

Normalised convolution keeps the sharp subject from bleeding into the
blurred background: blurred = (x·m ⊛ h) / (m ⊛ h), where m selects only the
pixels at least as far away as the layer.

The per-pixel blur amount (0 = in focus, 1 = max blur) comes from one of
* an ellipse the user places around the subject,
* a stereo disparity map (|d - d_focus|),
* a sharpness map: local energy of the Laplacian (high-frequency content),
  which is large only where the photo is already in focus.
Masks are feathered by a Gaussian convolution so the transition is soft.
"""

from __future__ import annotations

import numpy as np

from .fft import fast_convolve2d
from .filters import box_sum, disc, filter2d, gaussian
from .kernels import laplacian


def ellipse_mask(shape: tuple[int, int], center: tuple[float, float],
                 axes: tuple[float, float]) -> np.ndarray:
    """1 inside the ellipse with the given centre (row, col) and semi-axes (rows, cols)."""
    rr, cc = np.mgrid[0:shape[0], 0:shape[1]]
    ar, ac = max(axes[0], 1e-6), max(axes[1], 1e-6)
    return (((rr - center[0]) / ar) ** 2 + ((cc - center[1]) / ac) ** 2 <= 1.0).astype(float)


def sharpness_map(img: np.ndarray, window: int = 15) -> np.ndarray:
    """Local high-frequency energy sum_window (∇²x)², normalised to [0, 1]."""
    lap = filter2d(np.asarray(img, dtype=float), laplacian(3))
    energy = box_sum(lap * lap, window, window, "same") / (window * window)
    peak = float(energy.max())
    return energy / peak if peak > 0 else energy


def sharpness_mask(img: np.ndarray, window: int = 15, threshold: float = 0.2) -> np.ndarray:
    return (sharpness_map(img, window) >= threshold).astype(float)


def feather(mask: np.ndarray, sigma: float) -> np.ndarray:
    return np.clip(filter2d(mask, gaussian(sigma)), 0.0, 1.0) if sigma > 0 else mask.astype(float)


def amount_from_mask(mask: np.ndarray, feather_sigma: float = 4.0) -> np.ndarray:
    return 1.0 - feather(mask, feather_sigma)


def amount_from_disparity(disparity: np.ndarray, focus: float, span: float | None = None,
                          feather_sigma: float = 1.0) -> np.ndarray:
    """Blur from a stereo disparity map.

    A thin lens focused at Z_f blurs a point at depth Z into a circle whose
    diameter is proportional to |1/Z - 1/Z_f|. Disparity is d = f·B / Z, so
    the blur is simply proportional to |d - d_focus|.
    """
    dist = np.abs(np.asarray(disparity, dtype=float) - focus)
    span = span or float(dist.max()) or 1.0
    return feather(np.clip(dist / span, 0.0, 1.0), feather_sigma)


def _blur(x: np.ndarray, k: np.ndarray) -> np.ndarray:
    r0, r1 = k.shape[0] // 2, k.shape[1] // 2
    xp = np.pad(x, ((r0, r0), (r1, r1)), mode="edge")
    return fast_convolve2d(xp, k, "valid")


def lens_blur(img: np.ndarray, amount: np.ndarray, max_radius: float = 8.0,
              layers: int = 5) -> np.ndarray:
    """Blend ``layers`` disc-blurred copies; pixels with amount 0 stay untouched."""
    x = np.asarray(img, dtype=float)
    a = np.clip(np.asarray(amount, dtype=float), 0.0, 1.0) * (layers - 1)
    out = np.zeros_like(x)
    for level in range(layers):
        weight = np.clip(1.0 - np.abs(a - level), 0.0, 1.0)   # soft layer membership
        if not weight.any():
            continue
        radius = max_radius * level / max(layers - 1, 1)
        if radius < 0.5:
            out += weight * x
            continue
        k = disc(radius)
        support = np.clip(a - (level - 1), 0.0, 1.0)   # pixels at least this far away
        both = _blur(x * support + 1j * support, k)   # two real blurs in one FFT pass
        num, den = both.real, both.imag
        layer = np.where(den > 1e-6, num / np.maximum(den, 1e-6), x)
        out += weight * layer
    return out
