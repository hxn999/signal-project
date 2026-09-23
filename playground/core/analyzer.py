"""Causality, BIBO stability and DC-gain analysis of 2D kernels.

These are pure-NumPy helpers used by the AnalyzerPanel in the UI.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CausalityResult:
    """Result of a raster-scan causality test on a 2D kernel."""
    is_causal: bool
    origin: tuple[int, int]             # (row, col) of the kernel centre
    shift: tuple[int, int] | None       # (a, b) minimum shift to make it causal, or None


@dataclass(frozen=True)
class BIBOResult:
    """BIBO stability metrics for a 2D LTI system with impulse response *h*."""
    s_abs: float                        # S = ΣΣ|h[i,j]|  (absolute-sum of kernel)
    b_max: float                        # B = max|x|       (input bound)
    y_bound: float                      # theoretical worst-case |y| ≤ B·S
    y_actual_max: float                 # actual max|y|    (from the convolution output)
    is_bibo_stable: bool                # S < ∞  (always True for a finite kernel)


def check_causality(kernel: np.ndarray) -> CausalityResult:
    """Test causality under raster-scan ordering.

    A 2D kernel h[i, j] with origin at its centre is *causal* under raster-scan
    ordering when every non-zero element lies at or after the origin in raster
    order:  row > centre_row  OR  (row == centre_row AND col >= centre_col).

    If the kernel is non-causal, we compute the minimum origin shift ``(a, b)``
    such that translating the origin by (a, b) makes it causal.
    """
    k = np.asarray(kernel, dtype=np.float64)
    rows, cols = k.shape
    cr, cc = rows // 2, cols // 2  # canonical centre

    # Indices of all non-zero elements
    nz = np.argwhere(np.abs(k) > 1e-15)
    if nz.size == 0:
        return CausalityResult(True, (cr, cc), None)

    # Under raster-scan with origin (cr, cc), an element at (r, c) is causal if
    # (r - cr, c - cc) is >= (0, 0) in raster order, i.e. r > cr  or  (r == cr and c >= cc).
    non_causal_mask = (nz[:, 0] < cr) | ((nz[:, 0] == cr) & (nz[:, 1] < cc))
    is_causal = not non_causal_mask.any()

    if is_causal:
        return CausalityResult(True, (cr, cc), None)

    # Minimum shift: move the origin so that ALL non-zero elements are at or
    # after it in raster order.  The required origin is the raster-first non-zero
    # element (smallest row, then smallest col within that row).
    min_r = int(nz[:, 0].min())
    min_c_at_min_r = int(nz[nz[:, 0] == min_r, 1].min())
    shift = (min_r - cr, min_c_at_min_r - cc)
    return CausalityResult(False, (cr, cc), shift)


def compute_bibo(kernel: np.ndarray, input_matrix: np.ndarray,
                 output: np.ndarray | None) -> BIBOResult:
    """Compute BIBO stability metrics.

    For a finite-extent kernel the system is always BIBO stable.
    We report the bound  |y[m,n]| ≤ B · S  and compare it to the actual output.
    """
    k = np.asarray(kernel, dtype=np.float64)
    x = np.asarray(input_matrix, dtype=np.float64)

    s_abs = float(np.abs(k).sum())
    b_max = float(np.abs(x).max()) if x.size else 0.0
    y_bound = b_max * s_abs

    y_actual_max = 0.0
    if output is not None and output.size:
        y_actual_max = float(np.abs(output).max())

    return BIBOResult(
        s_abs=s_abs,
        b_max=b_max,
        y_bound=y_bound,
        y_actual_max=y_actual_max,
        is_bibo_stable=True,  # finite kernels are always BIBO stable
    )


def dc_gain(kernel: np.ndarray) -> float:
    """DC gain: G = ΣΣ h[i, j]."""
    return float(np.asarray(kernel, dtype=np.float64).sum())


def kernel_classification(kernel: np.ndarray) -> str:
    """Classify the kernel based on its DC gain.

    Returns 'Averaging' if the DC gain is significantly non-zero,
    'Differencing' if it is approximately zero.
    """
    g = dc_gain(kernel)
    return "Differencing" if abs(g) < 1e-9 else "Averaging"


def is_symmetric(kernel: np.ndarray) -> bool:
    """Check if a kernel is symmetric (h[i,j] == h[-i,-j])."""
    k = np.asarray(kernel, dtype=np.float64)
    return bool(np.allclose(k, k[::-1, ::-1]))


def conv_corr_difference(output_conv: np.ndarray | None,
                         output_corr: np.ndarray | None) -> float | None:
    """Max absolute difference between convolution and cross-correlation outputs.

    Returns None if either output is unavailable.
    """
    if output_conv is None or output_corr is None:
        return None
    if output_conv.shape != output_corr.shape:
        return None
    return float(np.abs(output_conv - output_corr).max())
