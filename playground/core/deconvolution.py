"""Image deconvolution: undoing a known blur with the convolution theorem.

A blurred image is y = x ⊛ h (+ noise). By the convolution theorem
Y[k] = X[k] H[k], so the blur can be undone by dividing spectra:
X̂[k] = Y[k] / H[k]  — the inverse filter.

Two practical guards, both plain spectrum arithmetic:
* eps: bins where |H| < eps are zeroed. There the blur wiped the
  frequency out, and dividing by ~0 only amplifies noise.
* K  : 1/H = H*/|H|², and adding K to |H|² caps the gain 1/|H| at about
  1/(2√K), a smooth version of the same idea. K = 0, eps = 0 is the pure inverse.

Multiplying DFTs performs *circular* convolution. A real photo is not periodic,
so the image is mirror-padded before the transform to keep the wrap from
dragging the opposite edge into the result.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .fft import fft2, fftshift, ifft2, kernel_otf
from .filters import disc, gaussian, motion

PSF_KINDS = ("Gaussian", "Motion", "Defocus (disc)", "Box")


def make_psf(kind: str, size: float, angle: float = 0.0) -> np.ndarray:
    if kind == "Gaussian":
        return gaussian(size)
    if kind == "Motion":
        return motion(int(round(size)), angle)
    if kind == "Defocus (disc)":
        return disc(size)
    if kind == "Box":
        n = max(1, int(round(size)))
        return np.full((n, n), 1.0 / (n * n))
    raise ValueError(f"unknown PSF {kind!r}")


def blur(x: np.ndarray, psf: np.ndarray, circular: bool = False) -> np.ndarray:
    """y = x ⊛ h (same size). Non-circular blur mirror-extends the edges first."""
    x = np.asarray(x, dtype=float)
    if circular:
        return np.real(ifft2(fft2(x) * kernel_otf(psf, x.shape)))
    ph, pw = psf.shape
    xp = np.pad(x, ((ph, ph), (pw, pw)), mode="symmetric")
    yp = np.real(ifft2(fft2(xp) * kernel_otf(psf, xp.shape)))
    return yp[ph:ph + x.shape[0], pw:pw + x.shape[1]]


def degrade(x: np.ndarray, psf: np.ndarray, noise_std: float = 0.0, circular: bool = False,
            seed: int = 0) -> np.ndarray:
    y = blur(x, psf, circular)
    if noise_std > 0:
        y = y + np.random.default_rng(seed).normal(0.0, noise_std, y.shape)
    return y


@dataclass(frozen=True)
class DeconvResult:
    restored: np.ndarray
    otf_mag: np.ndarray       # |H[k]|, centred, for display
    gain_mag: np.ndarray      # |G[k]| of the restoration filter, centred
    zeroed: float             # fraction of bins cut by eps


def inverse_filter(y: np.ndarray, psf: np.ndarray, eps: float = 1e-3, k: float = 0.0,
                   pad: bool = True) -> DeconvResult:
    """X̂ = Y · H* / (|H|² + K), with bins where |H| < eps set to 0."""
    y = np.asarray(y, dtype=float)
    ph, pw = (psf.shape if pad else (0, 0))
    yp = np.pad(y, ((ph, ph), (pw, pw)), mode="symmetric") if pad else y
    h = kernel_otf(psf, yp.shape)
    mag = np.abs(h)
    keep = mag >= max(eps, 1e-12)   # exact zeros of H can never be inverted
    g = np.zeros_like(h)
    g[keep] = np.conj(h[keep]) / (mag[keep] ** 2 + k)
    xp = np.real(ifft2(fft2(yp) * g))
    restored = xp[ph:ph + y.shape[0], pw:pw + y.shape[1]]
    return DeconvResult(restored, fftshift(mag), fftshift(np.abs(g)), float(1 - keep.mean()))
