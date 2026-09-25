"""Built-in synthetic test images, so every application works without a file."""

from __future__ import annotations

from typing import Callable

import numpy as np

from .filters import filter2d, gaussian


def _texture(shape: tuple[int, int], seed: int, sigma: float = 1.5) -> np.ndarray:
    noise = np.random.default_rng(seed).normal(size=shape)
    t = filter2d(noise, gaussian(sigma))
    return (t - t.min()) / max(float(t.max() - t.min()), 1e-12)


def shapes(size: int = 256) -> np.ndarray:
    """Gradient background with a disc, a square, a triangle and stripes."""
    h = w = size
    rr, cc = np.mgrid[0:h, 0:w] / size
    img = 60 + 60 * cc
    img[(rr - 0.3) ** 2 + (cc - 0.3) ** 2 < 0.15 ** 2] = 220
    img[(rr > 0.55) & (rr < 0.85) & (cc > 0.15) & (cc < 0.45)] = 30
    tri = (rr > 0.2) & (rr < 0.5) & (np.abs(cc - 0.72) < (rr - 0.2) * 0.6)
    img[tri] = 180
    stripes = (rr > 0.6) & (rr < 0.9) & (cc > 0.55) & (cc < 0.9)
    img[stripes] = np.where(np.sin(cc[stripes] * size * 0.8) > 0, 240, 20)
    return np.clip(img + 8 * _texture((h, w), 1), 0, 255)


def textured(size: int = 256) -> np.ndarray:
    """Richly textured scene (good for stereo matching and deconvolution)."""
    base = shapes(size)
    return np.clip(0.6 * base + 100 * _texture((size, size), 2, 1.0), 0, 255)


STAR = np.array([[0, 0, 1, 0, 0],
                 [0, 1, 1, 1, 0],
                 [1, 1, 1, 1, 1],
                 [0, 1, 1, 1, 0],
                 [0, 0, 1, 0, 0]], dtype=float)


def pattern_positions(size: int) -> list[tuple[int, int]]:
    s = size / 256
    return [(int(r * s), int(c * s)) for r, c in ((30, 40), (60, 180), (150, 90), (190, 200), (120, 150))]


def pattern_template(size: int = 256) -> np.ndarray:
    """The object planted by ``repeated_objects`` (a ring with a star inside)."""
    n = max(15, size // 10) | 1
    rr, cc = np.mgrid[0:n, 0:n] - n // 2
    ring = np.abs(np.hypot(rr, cc) - n * 0.4) < max(1.0, n * 0.07)
    t = np.where(ring, 230.0, 40.0)
    star = np.kron(STAR, np.ones((max(1, n // 7),) * 2))
    o = (n - star.shape[0]) // 2
    t[o:o + star.shape[0], o:o + star.shape[1]][star > 0] = 230
    return t


def repeated_objects(size: int = 256) -> np.ndarray:
    """Textured background with the pattern template planted several times (detection demo)."""
    img = 90 + 60 * _texture((size, size), 3, 3.0)
    t = pattern_template(size)
    n = t.shape[0]
    for i, (r, c) in enumerate(pattern_positions(size)):
        r, c = min(r, size - n), min(c, size - n)
        img[r:r + n, c:c + n] = t * (1.0 - 0.1 * i) + 10 * i   # brightness / contrast varies
    return np.clip(img, 0, 255)


def checkerboard(size: int = 256) -> np.ndarray:
    rr, cc = np.mgrid[0:size, 0:size] // max(1, size // 16)
    return np.where((rr + cc) % 2 == 0, 220.0, 35.0)


def zone_plate(size: int = 256) -> np.ndarray:
    """cos(k r²): frequency increases outward (reaching ~0.94π in the corners, just
    under Nyquist) — any downsampling makes aliasing obvious."""
    rr, cc = np.mgrid[0:size, 0:size] - size / 2
    return 127.5 + 127.5 * np.cos(np.pi * (rr ** 2 + cc ** 2) / (1.5 * size))


SAMPLES: dict[str, Callable[[int], np.ndarray]] = {
    "Shapes": shapes,
    "Textured scene": textured,
    "Repeated objects": repeated_objects,
    "Checkerboard": checkerboard,
    "Zone plate": zone_plate,
}
