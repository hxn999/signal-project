import numpy as np
import pytest
from PIL import Image

from playground.core.image_io import to_intensity
from playground.core.kernels import PRESETS, make_preset


@pytest.mark.parametrize("name", PRESETS)
@pytest.mark.parametrize("n", [3, 5, 7, 9])
def test_shapes(name, n):
    k = make_preset(name, n)
    assert k.shape == (n, n)
    assert np.isfinite(k).all()


@pytest.mark.parametrize("n", [3, 5, 9])
def test_dc_gains(n):
    for name in ("Box blur", "Gaussian blur", "Sharpen", "Identity", "Emboss"):
        assert make_preset(name, n).sum() == pytest.approx(1.0), name
    for name in ("Laplacian", "Sobel X", "Sobel Y", "Prewitt X", "Prewitt Y"):
        assert make_preset(name, n).sum() == pytest.approx(0.0), name


def test_classic_3x3():
    np.testing.assert_array_equal(make_preset("Sobel X"), [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    np.testing.assert_array_equal(make_preset("Emboss"), [[-2, -1, 0], [-1, 1, 1], [0, 1, 2]])
    np.testing.assert_allclose(make_preset("Gaussian blur") * 16, [[1, 2, 1], [2, 4, 2], [1, 2, 1]])


def test_bad_size():
    with pytest.raises(ValueError):
        make_preset("Box blur", 4)


def test_image_to_intensity():
    img = Image.new("RGBA", (200, 100), (0, 0, 0, 0))
    m = to_intensity(img, max_side=32)
    assert m.shape == (16, 32)
    assert m.min() == 255  # transparent -> white
    m = to_intensity(Image.new("RGB", (10, 10), (0, 0, 0)))
    assert m.shape == (10, 10) and m.max() == 0
