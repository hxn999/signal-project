import itertools

import numpy as np
import pytest

from playground.core.convolution import (
    PADDING_MODES,
    ConvolutionError,
    convolve2d,
    output_shape,
    pad_input,
)

rng = np.random.default_rng(0)


def naive(x, k, stride, padding, flip=True):
    """Double-loop reference implementation."""
    kh, kw = k.shape
    padded, _ = pad_input(x, kh, kw, padding)
    kk = k[::-1, ::-1] if flip else k
    oh = (padded.shape[0] - kh) // stride[0] + 1
    ow = (padded.shape[1] - kw) // stride[1] + 1
    out = np.zeros((oh, ow))
    for m in range(oh):
        for n in range(ow):
            r, c = m * stride[0], n * stride[1]
            total = 0.0
            for i in range(kh):
                for j in range(kw):
                    total += padded[r + i, c + j] * kk[i, j]
            out[m, n] = total
    return out


def full_convolution(x, k):
    """y[m, n] = sum_{i,j} x[i, j] h[m - i, n - j] straight from the definition."""
    H, W = x.shape
    kh, kw = k.shape
    y = np.zeros((H + kh - 1, W + kw - 1))
    for i in range(H):
        for j in range(W):
            y[i:i + kh, j:j + kw] += x[i, j] * k
    return y


@pytest.mark.parametrize(
    "padding,stride,kshape",
    list(itertools.product(PADDING_MODES, [(1, 1), (2, 1), (2, 3)], [(3, 3), (2, 2), (1, 4), (5, 3)])),
)
def test_matches_naive(padding, stride, kshape):
    x = rng.normal(size=(7, 9))
    k = rng.normal(size=kshape)
    res = convolve2d(x, k, stride, padding)
    np.testing.assert_allclose(res.output, naive(x, k, stride, padding))
    assert res.output.shape == output_shape(x.shape, k.shape, stride, padding)


@pytest.mark.parametrize("kshape", [(3, 3), (4, 4), (2, 5)])
def test_zero_padding_matches_definition(kshape):
    x = rng.normal(size=(6, 8))
    k = rng.normal(size=kshape)
    res = convolve2d(x, k, padding="zero")
    top, _, left, _ = res.pad
    full = full_convolution(x, k)
    kh, kw = kshape
    crop = full[kh - 1 - top: kh - 1 - top + 6, kw - 1 - left: kw - 1 - left + 8]
    np.testing.assert_allclose(res.output, crop)
    # valid mode is the fully-overlapping part of the full convolution
    valid = convolve2d(x, k, padding="valid").output
    np.testing.assert_allclose(valid, full[kh - 1: 6, kw - 1: 8])


def test_impulse_returns_kernel():
    k = rng.normal(size=(3, 3))
    x = np.zeros((7, 7))
    x[3, 3] = 1
    out = convolve2d(x, k, padding="zero").output
    np.testing.assert_allclose(out[2:5, 2:5], k)
    assert np.count_nonzero(out) == 9


def test_correlation_hook():
    x = rng.normal(size=(5, 5))
    k = rng.normal(size=(3, 3))
    corr = convolve2d(x, k, flip=False).output
    np.testing.assert_allclose(corr, naive(x, k, (1, 1), "zero", flip=False))
    sym = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]], float)
    np.testing.assert_allclose(convolve2d(x, sym).output, convolve2d(x, sym, flip=False).output)


def test_steps_reproduce_output():
    x = rng.normal(size=(6, 7))
    k = rng.normal(size=(3, 2))
    res = convolve2d(x, k, (2, 2), "reflect")
    assert res.num_steps == res.output.size
    for idx in range(res.num_steps):
        st = res.step(idx)
        assert st.patch.shape == k.shape
        assert st.products.sum() == pytest.approx(st.value)
        assert res.output[st.out_pos] == pytest.approx(st.value)
    with pytest.raises(IndexError):
        res.step(res.num_steps)


def test_errors():
    with pytest.raises(ConvolutionError):
        convolve2d(np.ones((2, 2)), np.ones((3, 3)), padding="valid")
    with pytest.raises(ConvolutionError):
        convolve2d(np.ones((4, 4)), np.ones((3, 3)), stride=(0, 1))
    with pytest.raises(ConvolutionError):
        convolve2d(np.ones((4, 4)), np.ones((3, 3)), padding="bogus")


def test_tiny_input_all_padding_modes():
    x = np.array([[5.0]])
    for padding in PADDING_MODES:
        if padding == "valid":
            continue
        out = convolve2d(x, np.ones((3, 3)), padding=padding).output
        assert out.shape == (1, 1)
