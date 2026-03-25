from __future__ import annotations

import streamlit as st


def render_sidebar() -> dict:
    st.sidebar.markdown("## VisionShield AI")
    st.sidebar.caption("Privacy-preserving image protection demo")

    mode = st.sidebar.radio(
        "Protection mode",
        ["Full encryption", "Selective protection"],
        index=0,
        help=(
            "**Full encryption** applies the complete three-stage chaos pipeline "
            "(seeded diffusion → structural permutation → nonlinear substitution) "
            "to every pixel. **Selective protection** targets only the detected "
            "sensitive regions, leaving the rest of the image intact."
        ),
    )

    _selective_only = mode != "Selective protection"

    protection_style = st.sidebar.selectbox(
        "Selective protection style",
        ["Encrypted sensitive regions", "Blur sensitive regions"],
        index=0,
        disabled=_selective_only,
        help=(
            "**Encrypted sensitive regions** applies the full chaos-based XOR "
            "transformation to the selected area — reversible with the same seed. "
            "**Blur sensitive regions** applies Gaussian blur for a softer, "
            "non-reversible privacy effect. "
            "*(Disabled in Full encryption mode — the entire frame is encrypted.)*"
        ),
    )

    seed = st.sidebar.text_input(
        "Master seed",
        value="20260325",
        help=(
            "Integer that initialises all pseudo-random chaos sequences in the "
            "pipeline (6D, 8D and 9D hyperchaotic systems). The exact same seed "
            "is required to reverse the protection — changing it produces a "
            "completely different scrambling pattern."
        ),
    )

    show_technical = st.sidebar.toggle(
        "Show technical details",
        value=True,
        help=(
            "Reveals the intermediate output of each encryption stage: "
            "Stage 1 (seeded chaotic diffusion), Stage 2 (structural pixel "
            "permutation), and Stage 3 (nonlinear S-box substitution)."
        ),
    )

    use_demo_image = st.sidebar.toggle(
        "Use built-in demo image",
        value=True,
        help=(
            "Use the packaged test image instead of uploading your own. "
            "Disable this toggle and upload a file below to test the "
            "pipeline on any image."
        ),
    )

    selective_mask = st.sidebar.toggle(
        "Enable selective mask",
        value=True,
        help=(
            "Activates region-of-interest detection to locate sensitive areas "
            "before applying selective protection. When disabled, the entire "
            "image is treated as a single undifferentiated region."
        ),
    )

    edge_overlay = st.sidebar.toggle(
        "Add preprocessing edge overlay",
        value=False,
        help=(
            "Blends a Canny edge-detection map into the processed input view. "
            "Useful to visualise which structural boundaries the pipeline "
            "operates on before applying the encryption stages."
        ),
    )

    _blur_only = _selective_only or protection_style != "Blur sensitive regions"

    blur_strength = st.sidebar.slider(
        "Blur strength",
        min_value=5,
        max_value=41,
        value=19,
        step=2,
        disabled=_blur_only,
        help=(
            "Kernel size for the Gaussian blur used in the 'Blur sensitive regions' "
            "protection style. Must be an odd number. Higher values produce stronger "
            "privacy at the cost of more detail loss in the protected area. "
            "*(Only active when Selective protection + Blur sensitive regions are both selected.)*"
        ),
    )

    resize_max = st.sidebar.select_slider(
        "Max image dimension",
        options=[720, 960, 1280, 1600],
        value=1280,
        help=(
            "Limits the longest edge of the image (in pixels) before it enters "
            "the pipeline. Lower values speed up processing; higher values "
            "preserve more detail in the protected output."
        ),
    )

    uploaded_file = st.sidebar.file_uploader(
        "Upload an image",
        type=["png", "jpg", "jpeg", "webp"],
        accept_multiple_files=False,
        help=(
            "Upload any PNG, JPG, JPEG or WebP image to run through the "
            "VisionShield AI pipeline. Make sure to disable 'Use built-in "
            "demo image' above so your file is used instead."
        ),
    )

    return {
        "mode": mode,
        "protection_style": protection_style,
        "seed": seed,
        "show_technical": show_technical,
        "use_demo_image": use_demo_image,
        "uploaded_file": uploaded_file,
        "selective_mask": selective_mask,
        "edge_overlay": edge_overlay,
        "blur_strength": blur_strength,
        "resize_max": resize_max,
    }