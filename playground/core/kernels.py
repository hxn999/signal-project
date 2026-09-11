"""Preset kernel library. Every generator takes an odd size n (>= 3)."""

from __future__ import annotations

from typing import Callable

import numpy as np

CLASSIC_SHARPEN = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]], dtype=float)


def _binomial(n: int) -> np.ndarray:
    row = np.array([1.0])
    for _ in range(n - 1):
        row = np.convolve(row, [1.0, 1.0])
    return row


def _delta(n: int) -> np.ndarray:
    k = np.zeros((n, n))
    k[n // 2, n // 2] = 1.0
    return k


def identity(n: int) -> np.ndarray:
    return _delta(n)


def box_blur(n: int) -> np.ndarray:
    return np.full((n, n), 1.0 / (n * n))


def gaussian_blur(n: int) -> np.ndarray:
    """Binomial approximation of a Gaussian (3×3 gives the classic [1 2 1]ᵀ[1 2 1]/16)."""
    b = _binomial(n)
    k = np.outer(b, b)
    return k / k.sum()


def sharpen(n: int) -> np.ndarray:
    if n == 3:
        return CLASSIC_SHARPEN.copy()
    return 2 * _delta(n) - gaussian_blur(n)  # unsharp mask


def laplacian(n: int) -> np.ndarray:
    k = -np.ones((n, n))
    k[n // 2, n // 2] = n * n - 1
    return k


def sobel_x(n: int) -> np.ndarray:
    smooth = _binomial(n)
    deriv = np.convolve(_binomial(n - 1), [-1.0, 1.0])
    return np.outer(smooth, deriv)


def sobel_y(n: int) -> np.ndarray:
    return sobel_x(n).T.copy()


def prewitt_x(n: int) -> np.ndarray:
    return np.outer(np.ones(n), np.arange(n) - n // 2).astype(float)


def prewitt_y(n: int) -> np.ndarray:
    return prewitt_x(n).T.copy()


def emboss(n: int) -> np.ndarray:
    i, j = np.indices((n, n))
    k = (i + j - (n - 1)).astype(float)
    k[n // 2, n // 2] = 1.0
    return k


# name -> (category, generator)
PRESETS: dict[str, tuple[str, Callable[[int], np.ndarray]]] = {
    "Identity": ("Basic", identity),
    "Box blur": ("Blur", box_blur),
    "Gaussian blur": ("Blur", gaussian_blur),
    "Sharpen": ("Sharpen", sharpen),
    "Laplacian": ("Edge detection", laplacian),
    "Sobel X": ("Edge detection", sobel_x),
    "Sobel Y": ("Edge detection", sobel_y),
    "Prewitt X": ("Edge detection", prewitt_x),
    "Prewitt Y": ("Edge detection", prewitt_y),
    "Emboss": ("Emboss", emboss),
}


def make_preset(name: str, n: int = 3) -> np.ndarray:
    if name not in PRESETS:
        raise KeyError(f"unknown preset {name!r}")
    if n < 3 or n % 2 == 0:
        raise ValueError("preset size must be an odd number >= 3")
    return PRESETS[name][1](n)
