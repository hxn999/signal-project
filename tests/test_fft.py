import numpy as np
import pytest

from playground.core.convolution import convolve2d
from playground.core.fft import (
    bit_reversed_indices,
    fast_convolve2d,
    fast_correlate2d,
    fft,
    fft2,
    fftshift,
    good_size,
    ifft,
    ifft2,
    kernel_otf,
    next_pow2,
)

rng = np.random.default_rng(1)


def rel_err(a, b):
    return np.abs(a - b).max() / max(np.abs(b).max(), 1e-300)


@pytest.mark.parametrize("n", [1, 2, 4, 8, 64, 256,          # radix-2
                               3, 6, 9, 12, 45, 100, 300,     # Cooley–Tukey mixed radix
                               5, 7, 13, 17, 127, 257])       # primes (direct / Bluestein)
def test_fft_matches_numpy(n):
    x = rng.normal(size=(3, n)) + 1j * rng.normal(size=(3, n))
    assert rel_err(fft(x), np.fft.fft(x)) < 1e-12
    assert rel_err(ifft(x), np.fft.ifft(x)) < 1e-12


def test_fft_along_other_axis():
    x = rng.normal(size=(12, 5))
    assert rel_err(fft(x, axis=0), np.fft.fft(x, axis=0)) < 1e-12


def test_round_trip():
    x = rng.normal(size=37)
    assert np.allclose(ifft(fft(x)), x)


def test_bit_reversal_order():
    assert bit_reversed_indices(8).tolist() == [0, 4, 2, 6, 1, 5, 3, 7]
    assert bit_reversed_indices(16)[3] == 12   # CT3 Q8: x[3] sits at position 12


def test_lecture_example():
    assert np.allclose(fft([1, 2, 3, 4]), [10, -2 + 2j, -2, -2 - 2j])


def test_parseval_and_conjugate_symmetry():
    x = rng.normal(size=24)
    X = fft(x)
    assert np.isclose((x ** 2).sum(), (np.abs(X) ** 2).sum() / 24)
    k = np.arange(24)
    assert np.allclose(X[(-k) % 24], np.conj(X))


def test_circular_shift_is_phase_only():
    x = rng.normal(size=16)
    X, Xs = fft(x), fft(np.roll(x, 3))
    assert np.allclose(np.abs(X), np.abs(Xs))
    assert np.allclose(Xs, np.exp(-2j * np.pi * np.arange(16) * 3 / 16) * X)


def test_fft2_matches_numpy():
    x = rng.normal(size=(30, 17))
    assert rel_err(fft2(x), np.fft.fft2(x)) < 1e-12
    assert np.allclose(ifft2(fft2(x)).real, x)


def test_fftshift_matches_numpy():
    x = rng.normal(size=(5, 8))
    assert np.array_equal(fftshift(x), np.fft.fftshift(x))


def test_sizes():
    assert next_pow2(1) == 1 and next_pow2(5) == 8 and next_pow2(8) == 8
    assert good_size(17) == 18 and good_size(544) == 576 and good_size(1021) == 1024
    for n in range(1, 300):
        g = good_size(n)
        m = g
        for p in (2, 3, 5):
            while m % p == 0:
                m //= p
        assert g >= n and m == 1


@pytest.mark.parametrize("mode,padding", [("same", "zero"), ("valid", "valid"), ("circular", "circular")])
@pytest.mark.parametrize("kshape", [(3, 3), (4, 2), (5, 7)])
def test_fast_convolution_matches_direct(mode, padding, kshape):
    x = rng.normal(size=(20, 23))
    k = rng.normal(size=kshape)
    assert np.allclose(fast_convolve2d(x, k, mode), convolve2d(x, k, padding=padding).output)


def test_full_convolution_matches_numpy_1d():
    x, h = np.array([[2, 4, 5, 6, 5, 3, 2, 1.0]]), np.array([[1, 2, 1.0]])
    assert np.allclose(fast_convolve2d(x, h), [[2, 8, 15, 20, 22, 19, 13, 8, 4, 1]])


def test_unpadded_product_is_circular():
    # lecture example: multiplying 8-point DFTs wraps the first two outputs
    x = np.array([2, 4, 5, 6, 5, 3, 2, 1.0])
    h = np.array([1, 2, 1, 0, 0, 0, 0, 0.0])
    assert np.allclose(ifft(fft(x) * fft(h)).real, [6, 9, 15, 20, 22, 19, 13, 8])


def test_complex_input_convolves_two_images():
    a, b, k = rng.normal(size=(9, 9)), rng.normal(size=(9, 9)), rng.normal(size=(3, 3))
    both = fast_convolve2d(a + 1j * b, k, "same")
    assert np.allclose(both.real, fast_convolve2d(a, k, "same"))
    assert np.allclose(both.imag, fast_convolve2d(b, k, "same"))


def test_correlation_is_unflipped():
    x, t = rng.normal(size=(12, 12)), rng.normal(size=(3, 4))
    assert np.allclose(fast_correlate2d(x, t), convolve2d(x, t, padding="valid", flip=False).output)


def test_kernel_otf_of_delta_is_flat():
    d = np.zeros((3, 3))
    d[1, 1] = 1
    assert np.allclose(kernel_otf(d, (8, 8)), 1)
