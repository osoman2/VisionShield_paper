from __future__ import annotations

import streamlit as st

from core.config import APP_DESCRIPTION, PAPER_TITLE, PAPER_URL
from core.flow_content import DISRUPTIVE_ANGLE, FLOW_STAGES, USE_CASES

_NODE_LABELS: dict[str, str] = {
    "Input":   "⬡  Input",
    "Stage 1": "① Diffusion",
    "Stage 2": "② Permutation",
    "Stage 3": "③ Substitution",
    "Output":  "⬡  Output",
}


def render_explanation_tab() -> None:
    st.markdown('<div class="panel-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Explanation workspace</div>', unsafe_allow_html=True)
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
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("### Source paper")
        st.link_button(PAPER_TITLE, PAPER_URL)

        st.markdown("### What the paper contributes")
        st.write(
            "The paper presents a three-stage hyperchaos-based image encryption pipeline using 6D, 8D and 9D systems, dynamic S-box generation, XOR-based protection, and FPGA implementation for strong speed gains."
        )

        st.markdown("### Why this demo adds more portfolio value")
        st.write(
            "Instead of only replicating equations and reporting security metrics, this application turns the idea into an explainable, interactive, and product-facing system."
        )

        st.markdown("### Possible use cases")
        for item in USE_CASES:
            st.markdown(f'<span class="tag">{item}</span>', unsafe_allow_html=True)

    st.markdown("### Disruptive angle")
    for point in DISRUPTIVE_ANGLE:
        st.write(f"- {point}")

    st.markdown("### Recommended pitch")
    st.write(
        "VisionShield AI is a privacy-preserving visual protection system inspired by advanced chaos-based image encryption research. It demonstrates how secure imaging ideas can be transformed into a product-ready, explainable AI portfolio artifact."
    )