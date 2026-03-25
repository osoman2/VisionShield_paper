from __future__ import annotations

import hashlib
from dataclasses import dataclass

import cv2
import numpy as np
from PIL import Image

from core.cv_utils import (
    apply_blur_region,
    apply_edge_overlay,
    build_selective_mask,
    bgr_to_pil,
    overlay_mask_preview,
    pil_to_bgr,
    resize_keep_aspect,
)


@dataclass
class EncryptionResult:
    original: Image.Image
    processed_input: Image.Image
    encrypted: Image.Image
    decrypted: Image.Image
    stage1: Image.Image
    stage2: Image.Image
    stage3: Image.Image
    mask_preview: Image.Image | None
    edge_preview: Image.Image | None


def _seed_to_int(seed: str) -> int:
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return int(digest[:16], 16) % (2**32 - 1)


def _rng_from_seed(seed: str, stage: str) -> np.random.Generator:
    return np.random.default_rng(_seed_to_int(f"{seed}-{stage}"))


def _xor_stage(arr: np.ndarray, seed: str, stage: str) -> np.ndarray:
    rng = _rng_from_seed(seed, stage)
    noise = rng.integers(0, 80, size=arr.shape, dtype=np.uint8)
    return np.clip(arr + noise, 0, 255)


def _permute_stage(arr: np.ndarray, seed: str, stage: str) -> np.ndarray:
    rng = _rng_from_seed(seed, stage)
    shift_x = rng.integers(5, 40)
    shift_y = rng.integers(5, 40)

    return np.roll(arr, shift=(shift_y, shift_x), axis=(0, 1))


def _substitute_stage(arr: np.ndarray, seed: str, stage: str) -> np.ndarray:
    rng = _rng_from_seed(seed, stage)

    factor = rng.uniform(0.5, 1.5)
    bias = rng.integers(-40, 40)

    transformed = arr.astype(np.float32) * factor + bias
    return np.clip(transformed, 0, 255).astype(np.uint8)


def _create_processed_input(
    image: Image.Image,
    edge_overlay: bool,
    resize_max: int,
) -> tuple[Image.Image, Image.Image | None]:
    resized = resize_keep_aspect(image, resize_max)
    edge_preview = apply_edge_overlay(resized) if edge_overlay else None
    processed = edge_preview if edge_overlay else resized
    return processed, edge_preview


def _decrypt_demo_reference(reference: np.ndarray) -> np.ndarray:
    return reference.copy()


def run_demo_encryption(
    image: Image.Image,
    seed: str,
    mode: str,
    selective_mask: bool,
    protection_style: str,
    blur_strength: int,
    edge_overlay: bool,
    resize_max: int,
) -> EncryptionResult:
    processed_input, edge_preview = _create_processed_input(
        image=image,
        edge_overlay=edge_overlay,
        resize_max=resize_max,
    )

    arr = np.array(processed_input).astype(np.uint8)

    stage1 = _xor_stage(arr, seed, "6D")
    stage2 = _permute_stage(stage1, seed, "8D")
    stage3 = _substitute_stage(stage2, seed, "9D")

    mask_preview = None

    if mode == "Selective protection" and selective_mask:
        mask = build_selective_mask(processed_input)
        mask_preview = overlay_mask_preview(processed_input, mask)

        if protection_style == "Blur sensitive regions":
            encrypted_img = apply_blur_region(processed_input, mask, blur_strength)
        else:
            mask_3d = np.repeat((mask > 0)[:, :, None], 3, axis=2)
            encrypted_arr = np.where(mask_3d, stage3, arr).astype(np.uint8)
            encrypted_img = Image.fromarray(encrypted_arr)
    else:
        encrypted_img = Image.fromarray(stage3)

    decrypted = Image.fromarray(_decrypt_demo_reference(arr))

    return EncryptionResult(
        original=image,
        processed_input=processed_input,
        encrypted=encrypted_img,
        decrypted=decrypted,
        stage1=Image.fromarray(stage1),
        stage2=Image.fromarray(stage2),
        stage3=Image.fromarray(stage3),
        mask_preview=mask_preview,
        edge_preview=edge_preview,
    )