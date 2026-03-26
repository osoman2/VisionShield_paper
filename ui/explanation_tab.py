from __future__ import annotations

import streamlit as st

from core.config import APP_DESCRIPTION, PAPER_TITLE, PAPER_URL
from core.flow_content import ADAPTATION_NOTES, FLOW_STAGES, USE_CASES

_NODE_LABELS: dict[str, str] = {
    "Input":   "⬡  Input",
    "Stage 1": "① Diffusion",
    "Stage 2": "② Permutation",
    "Stage 3": "③ Substitution",
    "Output":  "⬡  Output",
}


def render_explanation_tab() -> None:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">The paper and the adaptation</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-copy">{APP_DESCRIPTION}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("### Interactive flow diagram")
        st.caption("Click a node to inspect that stage of the pipeline.")

        selected_label = st.pills(
            "Pipeline stage",
            options=list(_NODE_LABELS.values()),
            default=list(_NODE_LABELS.values())[0],
            selection_mode="single",
            label_visibility="collapsed",
            width="stretch",
        )

        # Map display label back to FLOW_STAGES key (fallback to first key if deselected)
        label_to_key = {v: k for k, v in _NODE_LABELS.items()}
        selected_stage = label_to_key.get(selected_label or "", "Input")

        stage = FLOW_STAGES[selected_stage]
        st.markdown('<div class="mini-card">', unsafe_allow_html=True)
        st.markdown(f"**{stage['title']}**")
        st.write(stage["summary"])
        for item in stage["details"]:
            st.write(f"- {item}")
        if stage.get("paper_note"):
            st.info(f"**This demo:** {stage['paper_note']}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### Source paper")
        st.link_button(PAPER_TITLE, PAPER_URL)

        st.markdown("### What the paper actually does")
        st.markdown(
            "The paper proposes a **three-stage hyperchaos-based image encryption algorithm** implemented on FPGA:\n\n"
            "- **6D hyperchaotic system** drives the diffusion stage via XOR mixing, destroying pixel-level correlations\n"
            "- **8D hyperchaotic system** generates a permutation matrix to spatially shuffle pixel positions\n"
            "- **9D hyperchaotic system** produces a dynamic S-box for nonlinear byte substitution\n\n"
            "Higher-dimensional chaotic systems have more positive Lyapunov exponents, making them significantly "
            "harder to reconstruct than standard 3D or 4D chaotic maps. The FPGA implementation runs the three ODE "
            "solvers in parallel, achieving real-time encryption throughput."
        )

        st.markdown("### What this demo keeps and what it changes")
        st.markdown(f"*Why:* {ADAPTATION_NOTES['why']}")
        col_k, col_c = st.columns(2)
        with col_k:
            st.markdown("**✓ Kept from paper**")
            for item in ADAPTATION_NOTES["kept"]:
                st.write(f"- {item}")
        with col_c:
            st.markdown("**↻ Changed for software**")
            for item in ADAPTATION_NOTES["changed"]:
                st.write(f"- {item}")

        st.markdown("### Practical use cases")
        for item in USE_CASES:
            st.markdown(f'<span class="tag">{item}</span>', unsafe_allow_html=True)