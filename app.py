import streamlit as st

from core.config import APP_TITLE, APP_SUBTITLE
from core.demo_data import load_input_image
from ui.styles import inject_global_styles
from ui.sidebar import render_sidebar
from ui.demo_tab import render_demo_tab
from ui.analysis_tab import render_analysis_tab
from ui.explanation_tab import render_explanation_tab

st.set_page_config(
    page_title="VisionShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_styles()

st.markdown(
    f"""
    <div class="hero-card">
        <div class="eyebrow">PORTFOLIO SYSTEM DEMO</div>
        <h1>{APP_TITLE}</h1>
        <p>{APP_SUBTITLE}</p>
    </div>
    """,
    unsafe_allow_html=True,
)

sidebar_state = render_sidebar()
image = load_input_image(sidebar_state["uploaded_file"], sidebar_state["use_demo_image"])

tab_demo, tab_analysis, tab_explanation = st.tabs(
    ["Pipeline Demo", "Security Analysis", "The Paper"]
)

with tab_demo:
    render_demo_tab(
        image=image,
        mode=sidebar_state["mode"],
        seed=sidebar_state["seed"],
        selective_mask=sidebar_state["selective_mask"],
        show_technical=sidebar_state["show_technical"],
        protection_style=sidebar_state["protection_style"],
        blur_strength=sidebar_state["blur_strength"],
        edge_overlay=sidebar_state["edge_overlay"],
        resize_max=sidebar_state["resize_max"],
    )

with tab_analysis:
    render_analysis_tab(
        image=image,
        mode=sidebar_state["mode"],
        seed=sidebar_state["seed"],
        selective_mask=sidebar_state["selective_mask"],
        protection_style=sidebar_state["protection_style"],
        blur_strength=sidebar_state["blur_strength"],
        edge_overlay=sidebar_state["edge_overlay"],
        resize_max=sidebar_state["resize_max"],
    )

with tab_explanation:
    render_explanation_tab()