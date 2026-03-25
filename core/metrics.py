from __future__ import annotations

import cv2
import numpy as np
import pandas as pd
from PIL import Image


def image_entropy(image: Image.Image) -> float:
    arr = np.array(image.convert("L")).flatten()
    hist, _ = np.histogram(arr, bins=256, range=(0, 255), density=True)
    hist = hist[hist > 0]
    return float(-np.sum(hist * np.log2(hist)))


def mse(img_a: Image.Image, img_b: Image.Image) -> float:
    a = np.array(img_a).astype(np.float32)
    b = np.array(img_b).astype(np.float32)
    return float(np.mean((a - b) ** 2))


def psnr(img_a: Image.Image, img_b: Image.Image) -> float:
    m = mse(img_a, img_b)
    if m == 0:
        return 99.0
    return float(20 * np.log10(255.0 / np.sqrt(m)))


def edge_density(image: Image.Image) -> float:
    gray = np.array(image.convert("L"))
    edges = cv2.Canny(gray, 80, 180)
    return float(np.mean(edges > 0))


def channel_histogram_df(image: Image.Image) -> pd.DataFrame:
    arr = np.array(image)
    rows = []
    for idx, channel_name in enumerate(["R", "G", "B"]):
        hist, _ = np.histogram(arr[:, :, idx], bins=256, range=(0, 255))
        for i, value in enumerate(hist):
            rows.append({"intensity": i, "count": int(value), "channel": channel_name})
    return pd.DataFrame(rows)


def summarize_metrics(original: Image.Image, processed: Image.Image, encrypted: Image.Image, decrypted: Image.Image) -> dict:
    return {
        "Entropy (processed input)": round(image_entropy(processed), 4),
        "Entropy (protected output)": round(image_entropy(encrypted), 4),
        "MSE processed vs protected": round(mse(processed, encrypted), 2),
        "PSNR processed vs protected": round(psnr(processed, encrypted), 2),
        "MSE processed vs reconstructed": round(mse(processed, decrypted), 2),
        "PSNR processed vs reconstructed": round(psnr(processed, decrypted), 2),
        "Edge density (processed)": round(edge_density(processed), 4),
        "Edge density (protected)": round(edge_density(encrypted), 4),
    }