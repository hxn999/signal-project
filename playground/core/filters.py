"""Sampled 2D impulse responses and filtering helpers shared by the applications."""

from __future__ import annotations

import math

import numpy as np

from .convolution import PADDING_MODES, pad_amounts
from .fft import fast_convolve2d


def gaussian(sigma: float, radius: int | None = None) -> np.ndarray:
    """Sampled Gaussian h[i, j] ∝ exp(-(i² + j²) / 2σ²), normalised to DC gain 1."""
    if sigma <= 0:
        return np.ones((1, 1))
    r = int(math.ceil(3 * sigma)) if radius is None else int(radius)
    i = np.arange(-r, r + 1)
    g = np.exp(-(i * i) / (2 * sigma * sigma))
    k = np.outer(g, g)
    return k / k.sum()


def disc(radius: float) -> np.ndarray:
    """Pillbox (2D rect in the radius): a lens-defocus / bokeh impulse response."""
    if radius < 0.5:
        return np.ones((1, 1))
    r = int(math.ceil(radius))
    i, j = np.mgrid[-r:r + 1, -r:r + 1]
    k = (i * i + j * j <= radius * radius).astype(float)
    return k / k.sum()


def box(n: int) -> np.ndarray:
    return np.full((n, n), 1.0 / (n * n))


def triangle_1d(f: int) -> np.ndarray:
    """First-order-hold (linear interpolation) pulse of half-width f: rect ⊛ rect."""
    a = np.arange(2 * f - 1)
    return 1.0 - np.abs(a - (f - 1)) / f


def motion(length: int, angle_deg: float) -> np.ndarray:
    """Straight-line camera-shake blur of ``length`` pixels at ``angle_deg``."""
    length = max(1, int(length))
    if length == 1:
        return np.ones((1, 1))
    r = length // 2
    k = np.zeros((2 * r + 1, 2 * r + 1))
    theta = math.radians(angle_deg)
    for t in np.linspace(-(length - 1) / 2, (length - 1) / 2, 4 * length):
        row = int(round(r - t * math.sin(theta)))
        col = int(round(r + t * math.cos(theta)))
        k[row, col] += 1.0
    return k / k.sum()


def filter2d(x: np.ndarray, kernel: np.ndarray, boundary: str = "replicate") -> np.ndarray:
    """'Same'-size convolution x ⊛ h with a chosen boundary extension, via fast convolution."""
    x = np.asarray(x, dtype=float)
    kh, kw = kernel.shape
    top, bottom, left, right = pad_amounts(kh, kw, boundary)
    mode = PADDING_MODES[boundary]
    padded = np.pad(x, ((top, bottom), (left, right)), mode=mode) if mode else x
    # same padding scheme as convolve2d, so the result matches it exactly
    return fast_convolve2d(padded, kernel, "valid")


def box_sum(x: np.ndarray, h: int, w: int, mode: str = "valid") -> np.ndarray:
    """Sum of every h×w window.

    A box is rect = u[n] - u[n - B], so x ⊛ box = (x ⊛ u) - (x ⊛ u)[n - B]:
    accumulate (convolve with the unit step = running sum) and difference.
    mode 'same' zero-pads so the window is centred on each pixel.
    """
    x = np.asarray(x, dtype=float)
    if mode == "same":
        top, left = (h - 1) // 2, (w - 1) // 2
        x = np.pad(x, ((top, h - 1 - top), (left, w - 1 - left)))
    acc = np.zeros((x.shape[0] + 1, x.shape[1] + 1))
    acc[1:, 1:] = x.cumsum(axis=0).cumsum(axis=1)   # step response of the 2D accumulator
    return acc[h:, w:] - acc[:-h, w:] - acc[h:, :-w] + acc[:-h, :-w]


def mse(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.mean((np.asarray(a, float) - np.asarray(b, float)) ** 2))


def psnr(reference: np.ndarray, test: np.ndarray, peak: float = 255.0) -> float:
    """Peak signal-to-noise ratio in dB: 10 log10(peak² / error energy per pixel)."""
    e = mse(reference, test)
    return math.inf if e == 0 else 10 * math.log10(peak * peak / e)
