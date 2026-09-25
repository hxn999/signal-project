"""Core algorithms behind the Applications tab."""

import numpy as np
import pytest

from playground.core import compression, deconvolution, detection, edges, portrait, stereo, superres
from playground.core.filters import box_sum, disc, filter2d, gaussian, motion, psnr, triangle_1d
from playground.core.convolution import convolve2d
from playground.core.samples import SAMPLES, pattern_positions, pattern_template, repeated_objects

rng = np.random.default_rng(2)


# ---- filters ------------------------------------------------------------------------

@pytest.mark.parametrize("k", [gaussian(1.3), disc(3.2), motion(9, 30), np.ones((1, 1))])
def test_kernels_have_unit_dc_gain(k):
    assert np.isclose(k.sum(), 1.0)
    assert k.shape[0] % 2 == 1


def test_triangle_is_rect_convolved_with_rect():
    assert np.allclose(triangle_1d(3), np.convolve(np.ones(3), np.ones(3)) / 3)


@pytest.mark.parametrize("boundary", ["zero", "replicate", "reflect", "circular"])
def test_filter2d_matches_convolve2d(boundary):
    x, k = rng.normal(size=(15, 18)), rng.normal(size=(5, 3))
    assert np.allclose(filter2d(x, k, boundary), convolve2d(x, k, padding=boundary).output)


def test_box_sum():
    x = rng.normal(size=(10, 12))
    ones = np.ones((3, 4))
    assert np.allclose(box_sum(x, 3, 4), convolve2d(x, ones, padding="valid").output)
    assert np.allclose(box_sum(x, 3, 3, "same"), convolve2d(x, np.ones((3, 3)), padding="zero").output)


def test_samples_are_images():
    for make in SAMPLES.values():
        img = make(64)
        assert img.shape == (64, 64) and img.min() >= 0 and img.max() <= 255


# ---- compression ----------------------------------------------------------------------

def test_compression_keeping_everything_is_lossless():
    img = SAMPLES["Shapes"](64)
    res = compression.compress(img, 8, keep=1.0)
    assert np.allclose(res.reconstruction, img)
    assert res.ratio == pytest.approx(1.0) and res.energy_kept == pytest.approx(1.0)


def test_compression_quality_drops_with_fewer_coefficients():
    img = SAMPLES["Shapes"](64)
    scores = [compression.compress(img, 8, keep=k).psnr for k in (0.5, 0.2, 0.05)]
    assert scores[0] > scores[1] > scores[2]
    res = compression.compress(img, 8, keep=0.1)
    assert res.ratio == pytest.approx(10, rel=0.05)


def test_compression_energy_follows_parseval():
    # if the kept set were not conjugate-symmetric, taking the real part of the
    # inverse DFT would lose energy and this equality would fail
    img = rng.uniform(0, 255, (16, 16))
    res = compression.compress(img, None, keep=0.3)
    assert (res.reconstruction ** 2).sum() == pytest.approx(res.energy_kept * (img ** 2).sum())


def test_quantisation_and_whole_image_blocks():
    img = SAMPLES["Shapes"](60)             # not a multiple of 8, not a power of 2
    coarse = compression.compress(img, 8, compression.METHODS[1], step=80)
    fine = compression.compress(img, 8, compression.METHODS[1], step=2)
    assert coarse.kept < fine.kept and coarse.psnr < fine.psnr
    whole = compression.compress(img, None, keep=1.0)
    assert np.allclose(whole.reconstruction, img)


# ---- detection -----------------------------------------------------------------------

def test_planted_templates_are_found():
    img, t = repeated_objects(128), pattern_template(128)
    score = detection.ncc_map(img, t)
    hits = detection.find_matches(score, t.shape, 0.9, 10)
    found = {(m.row, m.col) for m in hits}
    assert found == set(pattern_positions(128))
    assert all(m.score > 0.99 for m in hits)


def test_ncc_is_invariant_to_brightness_and_contrast():
    t = rng.normal(size=(5, 5))
    img = rng.normal(size=(30, 30))
    img[10:15, 20:25] = 3 * t + 50
    score = detection.ncc_map(img, t)
    assert np.unravel_index(np.argmax(score), score.shape) == (10, 20)
    assert score.max() == pytest.approx(1.0)
    assert score.min() >= -1 and score.max() <= 1


# ---- deconvolution -------------------------------------------------------------------

def test_noise_free_circular_blur_is_inverted_exactly():
    x = rng.uniform(0, 255, (64, 64))
    psf = gaussian(1.0)
    y = deconvolution.degrade(x, psf, 0.0, circular=True)
    res = deconvolution.inverse_filter(y, psf, eps=0.0, k=0.0, pad=False)
    assert np.allclose(res.restored, x, atol=1e-6)


def test_regularised_inverse_improves_a_noisy_blur():
    x = SAMPLES["Textured scene"](128)
    psf = deconvolution.make_psf("Motion", 9, 45)
    y = deconvolution.degrade(x, psf, 0.5)
    res = deconvolution.inverse_filter(y, psf, eps=0.0, k=0.002)
    assert psnr(x, res.restored) > psnr(x, y) + 1.5


def test_exact_zeros_of_h_are_not_divided():
    x = rng.uniform(0, 255, (32, 32))
    psf = deconvolution.make_psf("Box", 4)          # box spectrum has exact zeros
    res = deconvolution.inverse_filter(deconvolution.blur(x, psf), psf, eps=0.0, k=0.0)
    assert np.isfinite(res.restored).all()


# ---- Canny ---------------------------------------------------------------------------

def test_canny_finds_a_thin_square_outline():
    img = np.zeros((40, 40))
    img[10:30, 10:30] = 200
    res = edges.canny(img, sigma=1.0, low=0.1, high=0.3)
    e = res.edges
    assert e[:, :5].sum() == 0 and e[15:25, 15:25].sum() == 0      # nothing far from edges
    for r in range(14, 26):                                          # every row crosses both sides
        cols = np.nonzero(e[r])[0]
        assert cols.size == 2 or r in (14, 25)   # corners may add a pixel
        assert abs(cols.min() - 9.5) <= 1.5 and abs(cols.max() - 29.5) <= 1.5


def test_hysteresis_keeps_only_connected_weak_pixels():
    strong = np.zeros((5, 7), bool)
    strong[2, 0] = True
    weak = np.zeros((5, 7), bool)
    weak[2, 1:4] = True     # chain touching the strong pixel
    weak[0, 6] = True       # isolated
    out = edges.hysteresis(strong, weak)
    assert out[2, :4].all() and not out[0, 6]


# ---- stereo --------------------------------------------------------------------------

def test_synthetic_pair_disparity_is_recovered():
    img = SAMPLES["Textured scene"](128)
    truth = stereo.default_disparity_layers(img.shape, 8)
    left, right = stereo.synthetic_pair(img, truth)
    res = stereo.disparity_map(left, right, 10, 7)
    inner = (slice(10, -10), slice(20, -10))
    assert np.mean(res.disparity[inner] == truth[inner]) > 0.85


def test_uniform_shift_gives_constant_disparity():
    left = rng.uniform(0, 255, (32, 48))
    right = np.roll(left, -3, axis=1)                       # right = L[n + 3]
    res = stereo.disparity_map(left, right, 6, 5)
    assert np.all(res.disparity[:, 8:-8] == 3)
    assert np.allclose(res.depth[:, 8:-8], 100 / 3)


# ---- portrait ------------------------------------------------------------------------

def test_in_focus_pixels_are_untouched():
    img = SAMPLES["Shapes"](64)
    amount = portrait.amount_from_mask(portrait.ellipse_mask(img.shape, (32, 32), (15, 10)), 2.0)
    out = portrait.lens_blur(img, amount, 5, 4)
    assert np.allclose(out[amount == 0], img[amount == 0])
    assert not np.allclose(out, img)


def test_uniform_image_stays_uniform():
    img = np.full((32, 32), 77.0)
    out = portrait.lens_blur(img, np.ones_like(img), 6, 3)
    assert np.allclose(out, 77.0)


def test_disparity_amount_is_zero_at_focus():
    disp = np.array([[2.0, 6.0, 10.0]])
    a = portrait.amount_from_disparity(disp, 6.0, feather_sigma=0)
    assert np.allclose(a, [[1.0, 0.0, 1.0]])


def test_sharpness_map_prefers_detail():
    img = np.full((40, 40), 100.0)
    img[5:15, 5:15] = rng.uniform(0, 255, (10, 10))
    s = portrait.sharpness_map(img, 5)
    assert s[10, 10] > 0.3 and s[30, 30] == pytest.approx(0)


# ---- super resolution ---------------------------------------------------------------

def test_sinc_upsampling_is_exact_for_bandlimited_images():
    n, f = 16, 3
    fine = np.arange(n * f) / f
    rr, cc = np.meshgrid(fine, fine, indexing="ij")
    signal = lambda r, c: 100 + 40 * np.cos(2 * np.pi * 3 * r / n) + 25 * np.sin(2 * np.pi * (2 * r + 5 * c) / n)
    low = signal(*np.meshgrid(np.arange(n), np.arange(n), indexing="ij"))
    assert np.allclose(superres.upsample_sinc(low, f), signal(rr, cc))


def test_zoh_repeats_samples_and_linear_interpolates():
    low = np.array([[0.0, 30.0], [60.0, 90.0]])
    assert np.allclose(superres.upsample_zoh(low, 2), np.kron(low, np.ones((2, 2))))
    lin = superres.upsample_linear(low, 2)
    assert lin[0, 0] == pytest.approx(0, abs=1e-9) and lin[0, 1] == pytest.approx(15) and lin[1, 1] == pytest.approx(45)


def test_antialiasing_matters_for_high_frequencies():
    img = SAMPLES["Zone plate"](128)
    ref = superres.ideal_lowpass(img, 2)          # the best any ×2 reconstruction can do
    good = superres.upsample_sinc(superres.downsample(img, 2, True), 2)
    bad = superres.upsample_sinc(superres.downsample(img, 2, False), 2)
    assert np.allclose(good, ref)
    assert psnr(ref, bad) < 20
