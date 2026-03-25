from __future__ import annotations

from io import BytesIO
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw

# Real-world demo: drone scene with sensitive faces — used when no file is uploaded
_DEMO_IMAGE_PATH = Path(__file__).parent.parent / "test_imgs" / "caras_drone.jpg"


def _fallback_demo_image(size: tuple[int, int] = (1280, 720)) -> Image.Image:
    """Generated placeholder used only when caras_drone.jpg is missing."""
    w, h = size
    img = Image.new("RGB", size, color=(10, 18, 30))
    draw = ImageDraw.Draw(img)

    for y in range(h):
        r = int(12 + 40 * (y / max(1, h - 1)))
        g = int(28 + 80 * (y / max(1, h - 1)))
        b = int(60 + 130 * (y / max(1, h - 1)))
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    draw.rounded_rectangle((70, 70, 450, 330), radius=24, outline=(255, 255, 255), width=4)
    draw.text((100, 110), "Privacy-critical region", fill=(255, 255, 255))
    draw.text((100, 160), "Face / Plate / Document / Sensor Overlay", fill=(220, 235, 255))

    draw.rounded_rectangle((520, 120, 1160, 560), radius=32, outline=(255, 255, 255), width=4)
    draw.text((590, 190), "Operational vision scene", fill=(255, 255, 255))
    draw.text((590, 250), "Inspection, drone, field, medical or industrial imagery", fill=(220, 235, 255))

    draw.rounded_rectangle((160, 470, 470, 650), radius=20, outline=(255, 255, 255), width=3)
    draw.text((210, 535), "Protected metadata area", fill=(255, 255, 255))

    return img


def load_input_image(uploaded_file: Optional[BytesIO], use_demo_image: bool) -> Image.Image:
    if uploaded_file is not None:
        return Image.open(uploaded_file).convert("RGB")
    if use_demo_image:
        if _DEMO_IMAGE_PATH.exists():
            return Image.open(_DEMO_IMAGE_PATH).convert("RGB")
        return _fallback_demo_image()
    return _fallback_demo_image()