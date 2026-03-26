from __future__ import annotations

import matplotlib.pyplot as plt
import streamlit as st

from core.crypto import run_demo_encryption
from core.metrics import channel_histogram_df, summarize_metrics


def render_analysis_tab(
    image,
    mode: str,
    seed: str,
    selective_mask: bool,
    protection_style: str,
    blur_strength: int,
    edge_overlay: bool,
    resize_max: int,
) -> None:
    result = run_demo_encryption(
        image=image,
        seed=seed,
        mode=mode,
        selective_mask=selective_mask,
        protection_style=protection_style,
        blur_strength=blur_strength,
        edge_overlay=edge_overlay,
        resize_max=resize_max,
    )

    metrics = summarize_metrics(
        original=result.original,
        processed=result.processed_input,
        encrypted=result.encrypted,
        decrypted=result.decrypted,
    )

    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Security metrics</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-copy">Standard cryptographic quality indicators measured on your image. '
        'Strong encryption raises entropy toward 8.0 bits, keeps PSNR low (high distortion from original), '
        'and flattens the histogram so no intensity value is predictable.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    cols = st.columns(4)
    items = list(metrics.items())
    for idx, (k, v) in enumerate(items):
        cols[idx % 4].metric(k, v)

    st.markdown("### RGB histograms")
    df_processed = channel_histogram_df(result.processed_input)
    df_protected = channel_histogram_df(result.encrypted)

    left, right = st.columns(2)

    with left:
        st.markdown("**Processed input histogram**")
        fig1, ax1 = plt.subplots(figsize=(8, 4))
        for ch in ["R", "G", "B"]:
            subset = df_processed[df_processed["channel"] == ch]
            ax1.plot(subset["intensity"], subset["count"], label=ch)
        ax1.set_xlabel("Intensity")
        ax1.set_ylabel("Count")
        ax1.legend()
        st.pyplot(fig1, width="stretch")

    with right:
        st.markdown("**Protected output histogram**")
        fig2, ax2 = plt.subplots(figsize=(8, 4))
        for ch in ["R", "G", "B"]:
            subset = df_protected[df_protected["channel"] == ch]
            ax2.plot(subset["intensity"], subset["count"], label=ch)
        ax2.set_xlabel("Intensity")
        ax2.set_ylabel("Count")
        ax2.legend()
        st.pyplot(fig2, width="stretch")

    st.markdown("### Reading these metrics")
    st.markdown(
        "- **Entropy** measures information density per pixel. A natural image scores ~7.0–7.5 bits; "
        "a well-encrypted image should reach ~7.9–8.0 bits as pixel values become statistically uniform.\n"
        "- **MSE** (Mean Squared Error) measures average pixel-level deviation. High MSE means the encrypted output "
        "is far from the original — which is what encryption is supposed to do.\n"
        "- **PSNR** (Peak Signal-to-Noise Ratio) is the inverse: low PSNR means high distortion. "
        "For encryption, low PSNR between input and encrypted is a good sign.\n"
        "- **Edge density** drops after encryption because spatial structure is destroyed — "
        "edges only exist when neighboring pixels are correlated.\n"
        "- The **histogram** of the encrypted image should be flat: every intensity value should appear with roughly equal frequency, "
        "which is the visual signature of a well-diffused ciphertext."
    )