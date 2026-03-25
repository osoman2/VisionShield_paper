import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: linear-gradient(180deg, #07101d 0%, #09111b 100%);
                color: #f5f7fb;
            }

            .hero-card {
                padding: 1.6rem 1.7rem;
                border-radius: 22px;
                background: linear-gradient(135deg, rgba(15,35,70,0.96), rgba(11,120,120,0.84));
                border: 1px solid rgba(130,180,255,0.28);
                margin-bottom: 1rem;
                box-shadow: 0 12px 28px rgba(0,0,0,0.28);
            }

            .hero-card h1 {
                margin: 0.2rem 0 0.7rem 0;
                font-size: 2.2rem;
                color: white;
            }

            .hero-card p {
                margin: 0;
                color: #dfebff;
                font-size: 1.02rem;
                line-height: 1.65;
            }

            .eyebrow {
                font-size: 0.8rem;
                letter-spacing: 0.08em;
                color: #cfd8ea;
                font-weight: 700;
            }

            .panel-card {
                background: rgba(18, 30, 49, 0.86);
                border: 1px solid rgba(150,180,220,0.14);
                border-radius: 18px;
                padding: 1rem 1rem 0.85rem 1rem;
                margin-bottom: 1rem;
            }

            .mini-card {
                background: rgba(14, 24, 38, 0.95);
                border: 1px solid rgba(150,180,220,0.10);
                border-radius: 16px;
                padding: 0.85rem 1rem;
                margin-bottom: 0.8rem;
            }

            .section-title {
                font-size: 1.06rem;
                font-weight: 700;
                margin-bottom: 0.5rem;
                color: #ffffff;
            }

            .section-copy {
                color: #dce6f8;
                line-height: 1.6;
            }

            .tag {
                display: inline-block;
                padding: 0.28rem 0.6rem;
                border-radius: 999px;
                margin: 0.2rem 0.35rem 0.2rem 0;
                background: rgba(57, 108, 255, 0.18);
                border: 1px solid rgba(121, 160, 255, 0.28);
                color: #e8f0ff;
                font-size: 0.84rem;
            }

            /* ── Pipeline-node pills ─────────────────────────────────────── */
            /* Selectors cover both testid variants used across Streamlit versions */

            div[data-testid="stPillsWidget"],
            div[data-testid="stPills"] {
                display: flex !important;
                flex-wrap: nowrap !important;
                align-items: center !important;
                gap: 0 !important;
                width: 100% !important;
            }

            /* Arrows injected between node wrappers */
            div[data-testid="stPillsWidget"] > div:not(:last-child)::after,
            div[data-testid="stPills"] > div:not(:last-child)::after {
                content: "→";
                color: #64748b;
                font-size: 1rem;
                line-height: 1;
                padding: 0 0.35rem;
                flex-shrink: 0;
                pointer-events: none;
            }

            /* Inactive node */
            div[data-testid="stPillsWidget"] button,
            div[data-testid="stPills"] button {
                border-radius: 8px !important;
                padding: 0.42rem 0.85rem !important;
                font-size: 0.82rem !important;
                font-weight: 600 !important;
                background: rgba(125, 211, 252, 0.10) !important;
                border: 1.5px solid rgba(125, 211, 252, 0.28) !important;
                color: #7dd3fc !important;
                transition: background 0.15s ease, border-color 0.15s ease,
                            box-shadow 0.15s ease !important;
                cursor: pointer !important;
                white-space: nowrap !important;
            }

            /* Hover */
            div[data-testid="stPillsWidget"] button:hover,
            div[data-testid="stPills"] button:hover {
                background: rgba(125, 211, 252, 0.20) !important;
                border-color: rgba(125, 211, 252, 0.55) !important;
            }

            /* Active / selected node */
            div[data-testid="stPillsWidget"] button[aria-selected="true"],
            div[data-testid="stPills"] button[aria-selected="true"] {
                background: rgba(34, 197, 94, 0.20) !important;
                border-color: #22c55e !important;
                color: #86efac !important;
                box-shadow: 0 0 14px rgba(34, 197, 94, 0.22) !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )