"""Image file -> pixel-intensity matrix."""

from __future__ import annotations

import numpy as np
from PIL import Image, ImageOps

IMAGE_FILTER = "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tif *.tiff *.webp)"
RESOLUTIONS = (16, 32, 64, 128, 256)


def to_intensity(img: Image.Image, max_side: int | None = None) -> np.ndarray:
    """Grayscale float64 matrix in [0, 255]; transparency is composited onto white."""
    img = ImageOps.exif_transpose(img)
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGBA")
        background = Image.new("RGBA", img.size, (255, 255, 255, 255))
        img = Image.alpha_composite(background, img)
    img = img.convert("L")
    if max_side and max(img.size) > max_side:
        scale = max_side / max(img.size)
        size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
        img = img.resize(size, Image.Resampling.LANCZOS)
    return np.asarray(img, dtype=np.float64)


def load_image_matrix(path: str, max_side: int | None = 64) -> np.ndarray:
    with Image.open(path) as img:
        img.load()
        return to_intensity(img, max_side)
