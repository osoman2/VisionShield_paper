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
    st.markdown('<div class="section-title">Encryption pipeline</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="section-copy">Mode: <strong>{mode}</strong> &nbsp;·&nbsp; '
        f'Protection: <strong>{protection_style}</strong> &nbsp;·&nbsp; '
        f'Seed: <code>{seed}</code> &nbsp;·&nbsp; '
        f'Edge overlay: <strong>{edge_overlay}</strong></div>',
        unsafe_allow_html=True,
    )
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
        st.image(result.original, caption="① Original input", width="stretch")
    with row1[1]:
        st.image(result.processed_input, caption="② Preprocessed (Canny edge-enhanced)", width="stretch")
    with row1[2]:
        st.image(result.encrypted, caption="③ Encrypted — diffusion → permutation → substitution", width="stretch")
    with row1[3]:
        st.image(result.decrypted, caption="④ Decrypted reference — pipeline is reversible", width="stretch")
    st.caption(
        "The same seed always produces the same encrypted output. "
        "Change the seed in the sidebar to see a completely different transformation."
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
        st.markdown("### Per-stage output")
        st.caption("Each column shows the image after that stage completes. Inspect how each transform degrades readability progressively.")
        s1, s2, s3 = st.columns(3)
        with s1:
            st.image(result.stage1, caption="After Stage 1: Diffusion (6D)", width="stretch")
        with s2:
            st.image(result.stage2, caption="After Stage 2: Permutation (8D)", width="stretch")
        with s3:
            st.image(result.stage3, caption="After Stage 3: Substitution (9D)", width="stretch")