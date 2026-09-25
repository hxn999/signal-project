"""Transform-coding image compression with the 2D DFT (JPEG idea, Fourier flavour).

The image is cut into B×B blocks, each block is taken to the frequency domain,
small coefficients are thrown away (or coarsely quantised), and the inverse DFT
rebuilds an approximation.

Bookkeeping uses two DFT properties:
* conjugate symmetry — a real block has X[-k] = X[k]*, so a conjugate pair of
  complex bins carries exactly 2 real numbers and a self-conjugate bin (DC,
  Nyquist) carries 1. The number of real values to store therefore equals the
  number of kept bins, and a full block needs B² numbers, same as its pixels.
* Parseval — sum |x|² = (1/N) sum |X|², so the fraction of spectral energy kept
  is the fraction of signal energy kept.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .fft import fft2, fftshift, freq_grid, ifft2
from .filters import mse, psnr

METHODS = ("Keep largest coefficients", "Frequency-weighted quantisation")


@dataclass(frozen=True)
class CompressionResult:
    reconstruction: np.ndarray
    kept_map: np.ndarray        # per block, centred: 1 where the bin was kept
    kept: int                   # real numbers stored
    total: int                  # pixels
    energy_kept: float          # fraction of spectral energy kept (Parseval)
    mse: float
    psnr: float
    block: tuple[int, int]

    @property
    def ratio(self) -> float:
        return self.total / max(self.kept, 1)


def _to_blocks(x: np.ndarray, bh: int, bw: int) -> np.ndarray:
    h, w = x.shape
    return x.reshape(h // bh, bh, w // bw, bw).transpose(0, 2, 1, 3)


def _from_blocks(b: np.ndarray) -> np.ndarray:
    nh, nw, bh, bw = b.shape
    return b.transpose(0, 2, 1, 3).reshape(nh * bh, nw * bw)


def _mirror(mask: np.ndarray) -> np.ndarray:
    """mask at the conjugate bin (-k1, -k2) of every block."""
    return np.roll(mask[..., ::-1, ::-1], (1, 1), axis=(-2, -1))


def compress(img: np.ndarray, block: int | None = 8, method: str = METHODS[0],
             keep: float = 0.1, step: float = 20.0) -> CompressionResult:
    """Compress ``img``.

    block  : block side, or None for one block covering the whole image
    keep   : fraction of bins kept (method 0)
    step   : base quantiser step for the DC bin (method 1); the step grows
             linearly with frequency so fine detail is quantised more coarsely
    """
    img = np.asarray(img, dtype=float)
    h, w = img.shape
    bh, bw = (h, w) if not block else (block, block)
    ph, pw = -h % bh, -w % bw
    x = np.pad(img, ((0, ph), (0, pw)), mode="edge")
    spec = fft2(_to_blocks(x, bh, bw))

    if method == METHODS[0]:
        mags = np.abs(spec)
        n_keep = max(1, int(round(keep * mags.size)))
        thresh = np.partition(mags.ravel(), mags.size - n_keep)[mags.size - n_keep]
        mask = mags >= thresh
        mask |= _mirror(mask)            # keep conjugate partners together
        coded = np.where(mask, spec, 0)
    else:
        k1, k2 = freq_grid((bh, bw))
        radius = np.sqrt((k1 / max(bh / 2, 1)) ** 2 + (k2 / max(bw / 2, 1)) ** 2)
        q = step * math.sqrt(bh * bw) / 8 * (1 + 4 * radius)   # scale with block energy
        coded = (np.round(spec.real / q) + 1j * np.round(spec.imag / q)) * q
        mask = coded != 0

    recon_blocks = np.real(ifft2(coded))
    recon = _from_blocks(recon_blocks)[:h, :w]
    energy_kept = float((np.abs(coded) ** 2).sum() / max((np.abs(spec) ** 2).sum(), 1e-300))
    kept_map = _from_blocks(fftshift(mask.astype(float)))[:h, :w]
    return CompressionResult(recon, kept_map, int(mask.sum()), h * w, energy_kept,
                             mse(img, recon), psnr(img, recon), (bh, bw))
