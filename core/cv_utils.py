from __future__ import annotations

import io
from typing import Optional

import cv2
import numpy as np
from PIL import Image


def pil_to_bgr(image: Image.Image) -> np.ndarray:
    rgb = np.array(image.convert("RGB"))
    return cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)


def bgr_to_pil(image_bgr: np.ndarray) -> Image.Image:
    rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    return Image.fromarray(rgb)


def resize_keep_aspect(image: Image.Image, max_dim: int = 1280) -> Image.Image:
    w, h = image.size
    current_max = max(w, h)
    if current_max <= max_dim:
        return image

    scale = max_dim / current_max
    new_w = int(w * scale)
    new_h = int(h * scale)

    bgr = pil_to_bgr(image)
    resized = cv2.resize(bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return bgr_to_pil(resized)


def build_selective_mask(image: Image.Image) -> np.ndarray:
    """
    Más pro que un simple rectángulo:
    compone dos regiones elípticas + una franja rectangular
    para simular zonas sensibles como rostro, placa o documento.
    """
    w, h = image.size
    mask = np.zeros((h, w), dtype=np.uint8)

    cv2.ellipse(
        mask,
        center=(int(w * 0.23), int(h * 0.34)),
        axes=(int(w * 0.12), int(h * 0.16)),
        angle=0,
        startAngle=0,
        endAngle=360,
        color=255,
        thickness=-1,
    )

    cv2.rectangle(
        mask,
        (int(w * 0.12), int(h * 0.58)),
        (int(w * 0.42), int(h * 0.74)),
        color=255,
        thickness=-1,
    )

    cv2.ellipse(
        mask,
        center=(int(w * 0.72), int(h * 0.46)),
        axes=(int(w * 0.10), int(h * 0.12)),
        angle=18,
        startAngle=0,
        endAngle=360,
        color=255,
        thickness=-1,
    )

    kernel = np.ones((11, 11), np.uint8)
    mask = cv2.GaussianBlur(mask, (21, 21), 0)
    mask = cv2.dilate(mask, kernel, iterations=1)
    _, mask = cv2.threshold(mask, 32, 255, cv2.THRESH_BINARY)

    return mask


def overlay_mask_preview(image: Image.Image, mask: np.ndarray) -> Image.Image:
    bgr = pil_to_bgr(image)
    overlay = bgr.copy()
    overlay[mask > 0] = (20, 30, 230)

    composed = cv2.addWeighted(bgr, 0.70, overlay, 0.30, 0)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(composed, contours, -1, (255, 255, 255), 2)

    return bgr_to_pil(composed)


def apply_edge_overlay(image: Image.Image) -> Image.Image:
    bgr = pil_to_bgr(image)
    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 80, 180)

    edge_rgb = np.zeros_like(bgr)
    edge_rgb[:, :, 1] = edges
    blended = cv2.addWeighted(bgr, 0.88, edge_rgb, 0.42, 0)

    return bgr_to_pil(blended)


def apply_blur_region(image: Image.Image, mask: np.ndarray, blur_strength: int) -> Image.Image:
    if blur_strength % 2 == 0:
        blur_strength += 1
    blur_strength = max(3, blur_strength)

    bgr = pil_to_bgr(image)
    blurred = cv2.GaussianBlur(bgr, (blur_strength, blur_strength), 0)

    mask_3d = np.repeat((mask > 0)[:, :, None], 3, axis=2)
    merged = np.where(mask_3d, blurred, bgr)

    return bgr_to_pil(merged.astype(np.uint8))