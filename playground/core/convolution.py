"""2D convolution with stride and padding, plus per-step introspection.

The result object keeps everything the UI needs to replay the computation one
output sample at a time (window position, patch, products and sum).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

# UI key -> numpy.pad mode (None = no padding)
PADDING_MODES: dict[str, str | None] = {
    "valid": None,
    "zero": "constant",
    "reflect": "reflect",
    "replicate": "edge",
    "circular": "wrap",
}

PADDING_LABELS: dict[str, str] = {
    "valid": "Valid (no padding)",
    "zero": "Zero",
    "reflect": "Reflect",
    "replicate": "Replicate (edge)",
    "circular": "Circular (wrap)",
}


class ConvolutionError(ValueError):
    """Raised when the input / kernel / parameters cannot be convolved."""


@dataclass(frozen=True)
class Step:
    index: int
    out_pos: tuple[int, int]        # (m, n) in the output
    window_origin: tuple[int, int]  # top-left of the window in padded coords
    patch: np.ndarray               # padded input under the window
    products: np.ndarray            # patch * applied_kernel
    value: float                    # sum of products == output[m, n]


@dataclass(frozen=True)
class ConvResult:
    input: np.ndarray
    kernel: np.ndarray              # kernel as defined by the user, h[i, j]
    applied_kernel: np.ndarray      # kernel actually slid over the input
    padded: np.ndarray
    pad: tuple[int, int, int, int]  # top, bottom, left, right
    stride: tuple[int, int]
    padding: str
    flip: bool
    output: np.ndarray

    @property
    def num_steps(self) -> int:
        return int(self.output.size)

    def step(self, index: int) -> Step:
        if not 0 <= index < self.num_steps:
            raise IndexError(f"step {index} out of range 0..{self.num_steps - 1}")
        m, n = divmod(index, self.output.shape[1])
        r0, c0 = m * self.stride[0], n * self.stride[1]
        kh, kw = self.applied_kernel.shape
        patch = self.padded[r0:r0 + kh, c0:c0 + kw]
        products = patch * self.applied_kernel
        return Step(index, (m, n), (r0, c0), patch, products, float(self.output[m, n]))


def pad_amounts(kh: int, kw: int, padding: str) -> tuple[int, int, int, int]:
    """'Same'-style padding amounts; even kernels pad one extra on the bottom/right."""
    if padding not in PADDING_MODES:
        raise ConvolutionError(f"unknown padding mode {padding!r}")
    if PADDING_MODES[padding] is None:
        return (0, 0, 0, 0)
    top, left = (kh - 1) // 2, (kw - 1) // 2
    return (top, kh - 1 - top, left, kw - 1 - left)


def pad_input(x: np.ndarray, kh: int, kw: int,
              padding: str) -> tuple[np.ndarray, tuple[int, int, int, int]]:
    pad = pad_amounts(kh, kw, padding)
    mode = PADDING_MODES[padding]
    if mode is None or not any(pad):
        return x.copy(), pad
    top, bottom, left, right = pad
    return np.pad(x, ((top, bottom), (left, right)), mode=mode), pad


def output_shape(in_shape: tuple[int, int], k_shape: tuple[int, int],
                 stride: tuple[int, int], padding: str) -> tuple[int, int]:
    top, bottom, left, right = pad_amounts(*k_shape, padding)
    hp, wp = in_shape[0] + top + bottom, in_shape[1] + left + right
    kh, kw = k_shape
    if hp < kh or wp < kw:
        what = "padded input" if top + bottom + left + right else "input"
        raise ConvolutionError(f"kernel {kh}×{kw} is larger than the {what} {hp}×{wp}")
    return (hp - kh) // stride[0] + 1, (wp - kw) // stride[1] + 1


def convolve2d(x, k, stride=(1, 1), padding: str = "zero", flip: bool = True) -> ConvResult:
    """y[m, n] = sum_{i,j} x_pad[m*sh + i, n*sw + j] * k_applied[i, j].

    With ``flip=True`` k_applied = k[::-1, ::-1] (true convolution, the kernel
    is the impulse response). ``flip=False`` gives cross-correlation.
    """
    x = np.asarray(x, dtype=np.float64)
    k = np.asarray(k, dtype=np.float64)
    if x.ndim != 2 or x.size == 0:
        raise ConvolutionError("input must be a non-empty 2D matrix")
    if k.ndim != 2 or k.size == 0:
        raise ConvolutionError("kernel must be a non-empty 2D matrix")
    sh, sw = (int(s) for s in stride)
    if sh < 1 or sw < 1:
        raise ConvolutionError("stride must be at least 1")

    output_shape(x.shape, k.shape, (sh, sw), padding)  # validates sizes
    applied = k[::-1, ::-1].copy() if flip else k.copy()
    padded, pad = pad_input(x, *k.shape, padding)
    windows = sliding_window_view(padded, k.shape)[::sh, ::sw]
    out = np.einsum("mnij,ij->mn", windows, applied)
    return ConvResult(x, k, applied, padded, pad, (sh, sw), padding, flip, out)
