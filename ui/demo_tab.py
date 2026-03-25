from __future__ import annotations

import streamlit as st

from core.crypto import run_demo_encryption


def render_demo_tab(
    image,
    mode: str,
    seed: str,
    selective_mask: bool,
    show_technical: bool,
    protection_style: str,
    blur_strength: int,
    edge_overlay: bool,
    resize_max: int,
) -> None:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Interactive privacy demo</div>', unsafe_allow_html=True)
    
    st.markdown(
        '<div class="section-copy">This view shows the original image, the processed input used by the pipeline, the protected result, and a reversible reference output for portfolio storytelling.</div>',
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)

    st.markdown("### What you are seeing")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        **Pipeline overview**
        - The system preprocesses the image
        - Applies a multi-stage transformation
        - Protects either the full image or sensitive regions
        - Produces a privacy-safe visual output
        """)

    with col_b:
        st.markdown(f"""
        **Current configuration**
        - Mode: `{mode}`
        - Protection: `{protection_style}`
        - Seed: `{seed}`
        - Edge overlay: `{edge_overlay}`
        """)

    st.markdown("</div>", unsafe_allow_html=True)
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

    row1 = st.columns(4)
    with row1[0]:
        st.image(result.original, caption="Original input", width="stretch")
    with row1[1]:
        st.image(result.processed_input, caption="Processed view", width="stretch")
    with row1[2]:
        st.image(result.encrypted, caption="Protected image", width="stretch")
    with row1[3]:
        st.image(result.decrypted, caption="Reference restoration (demo)", width="stretch")
    st.caption(
    "The protected image is intentionally transformed to reduce visual readability, "
    "simulating privacy-preserving encryption. The reference restoration illustrates "
    "recoverability for demonstration purposes."
    )
    if result.mask_preview is not None or result.edge_preview is not None:
        st.markdown("### Visual aids")
        aux_cols = st.columns(2)

        with aux_cols[0]:
            if result.mask_preview is not None:
                st.markdown("### Sensitive regions")
                st.image(
                    result.mask_preview,
                    caption="Detected / simulated sensitive regions",
                    width="stretch",
                )

        with aux_cols[1]:
            if result.edge_preview is not None:
                st.image(result.edge_preview, caption="Edge-enhanced preprocessing view", width="stretch")

    if show_technical:
        st.markdown("### Internal three-stage preview")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.image(result.stage1, caption="Stage 1", width="stretch")
        with s2:
            st.image(result.stage2, caption="Stage 2", width="stretch")
        with s3:
            st.image(result.stage3, caption="Stage 3", width="stretch")

    st.success(
        "VisionShield AI reframes image encryption as a product system. "
        "Instead of focusing only on cryptographic strength, it demonstrates "
        "how privacy, computer vision, and explainability can be integrated "
        "into a usable visual pipeline."
    )