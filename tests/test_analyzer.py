"""Unit tests for playground.core.analyzer."""

import numpy as np
import pytest

from playground.core.analyzer import (
    check_causality,
    compute_bibo,
    conv_corr_difference,
    dc_gain,
    is_symmetric,
    kernel_classification,
)


# ---- Causality ----------------------------------------------------------- #

class TestCausality:
    def test_identity_is_causal(self):
        """Identity kernel: only the centre is non-zero → causal."""
        k = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]], dtype=float)
        r = check_causality(k)
        assert r.is_causal is True
        assert r.shift is None

    def test_laplacian_is_not_causal(self):
        """Standard Laplacian has non-zero elements before the centre."""
        k = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=float)
        r = check_causality(k)
        assert r.is_causal is False
        assert r.shift is not None

    def test_lower_right_kernel_is_causal(self):
        """Kernel with values only at and after centre → causal."""
        k = np.zeros((3, 3))
        k[1, 1] = 1.0
        k[1, 2] = 0.5
        k[2, 0] = 0.5
        k[2, 2] = 0.5
        r = check_causality(k)
        assert r.is_causal is True

    def test_zero_kernel(self):
        k = np.zeros((3, 3))
        r = check_causality(k)
        assert r.is_causal is True

    def test_shift_values(self):
        """A kernel with only top-left element non-zero needs shift (-1, -1)."""
        k = np.zeros((3, 3))
        k[0, 0] = 1.0
        r = check_causality(k)
        assert r.is_causal is False
        assert r.shift == (-1, -1)


# ---- BIBO stability ------------------------------------------------------ #

class TestBIBO:
    def test_basic_bibo(self):
        k = np.array([[1, 2], [3, 4]], dtype=float)
        x = np.ones((4, 4)) * 5.0
        out = np.full((3, 3), 50.0)
        r = compute_bibo(k, x, out)
        assert r.is_bibo_stable is True
        assert r.s_abs == pytest.approx(10.0)
        assert r.b_max == pytest.approx(5.0)
        assert r.y_bound == pytest.approx(50.0)
        assert r.y_actual_max == pytest.approx(50.0)

    def test_bibo_no_output(self):
        k = np.array([[1, -1]], dtype=float)
        x = np.ones((2, 2))
        r = compute_bibo(k, x, None)
        assert r.y_actual_max == 0.0
        assert r.is_bibo_stable is True


# ---- DC gain & classification -------------------------------------------- #

class TestDCGain:
    def test_box_blur_gain(self):
        """Box blur 3×3 sums to 1."""
        k = np.full((3, 3), 1.0 / 9.0)
        assert dc_gain(k) == pytest.approx(1.0)
        assert kernel_classification(k) == "Averaging"

    def test_laplacian_gain_zero(self):
        k = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=float)
        assert dc_gain(k) == pytest.approx(0.0)
        assert kernel_classification(k) == "Differencing"


# ---- Symmetry ------------------------------------------------------------ #

class TestSymmetry:
    def test_symmetric_kernel(self):
        k = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], dtype=float)
        assert is_symmetric(k) is True

    def test_asymmetric_kernel(self):
        k = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
        assert is_symmetric(k) is False


# ---- Conv vs Corr difference --------------------------------------------- #

class TestConvCorrDifference:
    def test_symmetric_gives_zero(self):
        out = np.ones((3, 3))
        assert conv_corr_difference(out, out) == pytest.approx(0.0)

    def test_different_outputs(self):
        a = np.array([[1.0, 2.0], [3.0, 4.0]])
        b = np.array([[4.0, 3.0], [2.0, 1.0]])
        assert conv_corr_difference(a, b) == pytest.approx(3.0)

    def test_none_inputs(self):
        assert conv_corr_difference(None, np.ones((2, 2))) is None
        assert conv_corr_difference(np.ones((2, 2)), None) is None
