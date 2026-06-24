"""Shared UI theme, branding and layout helpers for the Bakhteyar-AI Streamlit app.

Keeping the CSS and the sidebar / top-bar / footer markup in one place keeps the
three pages consistent and makes the design easy to tweak in a single spot.

PATCHED: Fixed SVG icons, Google Fonts loading, and Streamlit selector resilience.
"""

from datetime import datetime

import streamlit as st

# ----------------------------------------------------------------------------
# BRAND MARKS (pure CSS / inline SVG so there are no image assets to ship)
# ----------------------------------------------------------------------------

BRAND_MARK = (
    '<svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<rect width="44" height="44" rx="13" fill="url(#bv_grad_mark)"/>'
    '<rect x="10" y="16" width="4" height="12" rx="2" fill="#fff" opacity="0.8">'
    '<animate attributeName="height" values="12;22;12" dur="1.3s" repeatCount="indefinite"/>'
    '<animate attributeName="y" values="16;11;16" dur="1.3s" repeatCount="indefinite"/>'
    '</rect>'
    '<rect x="17" y="11" width="4" height="22" rx="2" fill="#fff">'
    '<animate attributeName="height" values="22;12;22" dur="1.3s" repeatCount="indefinite"/>'
    '<animate attributeName="y" values="11;16;11" dur="1.3s" repeatCount="indefinite"/>'
    '</rect>'
    '<rect x="24" y="14" width="4" height="16" rx="2" fill="#fff" opacity="0.9">'
    '<animate attributeName="height" values="16;22;16" dur="1.3s" repeatCount="indefinite"/>'
    '<animate attributeName="y" values="14;11;14" dur="1.3s" repeatCount="indefinite"/>'
    '</rect>'
    '<rect x="31" y="18" width="4" height="10" rx="2" fill="#fff" opacity="0.7">'
    '<animate attributeName="height" values="10;18;10" dur="1.3s" repeatCount="indefinite"/>'
    '<animate attributeName="y" values="18;13;18" dur="1.3s" repeatCount="indefinite"/>'
    '</rect>'
    '<defs><linearGradient id="bv_grad_mark" x1="0" y1="0" x2="44" y2="44">'
    '<stop offset="0%" stop-color="#7c3aed"/>'
    '<stop offset="50%" stop-color="#6366f1"/>'
    '<stop offset="100%" stop-color="#db2777"/>'
    '</linearGradient></defs>'
    '</svg>'
)

TRANSLATION_ICON = (
    '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M13 '
    '18l2-4 2 4m-3-2h4" stroke="#fff" stroke-width="2" stroke-linecap="round" '
    'stroke-linejoin="round"/>'
    '<path d="M12 12l-3 7" stroke="#fff" stroke-width="2" stroke-linecap="round"/>'
    '</svg>'
)

TTS_ICON = (
    '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M12 3v18m-4-14v10M4 9v6m16-6v6m-4-10v14" stroke="#fff" '
    'stroke-width="2" stroke-linecap="round"/>'
    '</svg>'
)

# ----------------------------------------------------------------------------
# GOOGLE FONTS (injected as <link> for reliability, not @import in <style>)
# ----------------------------------------------------------------------------

FONTS_LINK = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@600;700;800&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap" rel="stylesheet">"""

# ----------------------------------------------------------------------------
# THEME CSS
# ----------------------------------------------------------------------------

THEME_CSS = """
<style>
:root {
    --bv-ink: #1e1b2e;
    --bv-muted: #6b6783;
    --bv-border: rgba(124, 58, 237, 0.14);
    --bv-card: #ffffff;
    --bv-soft: #f5f3ff;
    --bv-purple: #7c3aed;
    --bv-purple-2: #6d28d9;
    --bv-indigo: #4f46e5;
    --bv-pink: #db2777;
    --bv-grad: linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #db2777 100%);
    --bv-radius: 20px;
    --bv-shadow: 0 18px 40px -18px rgba(79, 70, 229, 0.45);
}

html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"],
.main, .stMainBlockContainer {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--bv-ink);
}

/* Soft ambient background glow */
[data-testid="stAppViewContainer"], .stApp {
    background:
        radial-gradient(900px 500px at 12% -10%, rgba(124, 58, 237, 0.10), transparent 60%),
        radial-gradient(800px 500px at 100% 0%, rgba(219, 39, 119, 0.08), transparent 55%),
        #ffffff;
}

/* Hide Streamlit chrome (multiple selectors for version resilience) */
#MainMenu, header[data-testid="stHeader"], footer,
.stDeployButton, [data-testid="stToolbar"],
header.stAppHeader { visibility: hidden; height: 0; }

.block-container, .stMainBlockContainer {
    padding-top: 2.6rem;
    padding-bottom: 3rem;
    max-width: 940px;
}

h1, h2, h3, .bv-hero-title, .bv-brand-name, .bv-side-title {
    font-family: 'Sora', 'Inter', sans-serif;
}

/* ---------- Hide default sidebar nav ---------- */
[data-testid="stSidebarNav"], .stSidebarNav { display: none !important; }

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"], .stSidebar {
    background: linear-gradient(180deg, #2a1758 0%, #4c1d95 55%, #6d28d9 100%) !important;
    border-right: none !important;
}
section[data-testid="stSidebar"] *, .stSidebar * { color: #f3eaff !important; }

div[data-testid="stSidebarUserContent"] { padding-top: 1rem; }

.bv-side-brand {
    display: flex; align-items: center; gap: 12px;
    padding: 6px 6px 4px 6px;
}
.bv-side-title { font-size: 1.25rem; font-weight: 800; line-height: 1; }
.bv-side-sub { font-size: 0.78rem; opacity: 0.7; margin: 14px 6px 10px 6px; letter-spacing: 0.04em; text-transform: uppercase; }

section[data-testid="stSidebar"] div[data-testid="stPageLink"] a,
.stSidebar div[data-testid="stPageLink"] a {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 14px !important;
    margin: 7px 4px !important;
    padding: 11px 14px !important;
    font-weight: 600 !important;
    justify-content: flex-start !important;
    transition: all 0.18s ease !important;
}
section[data-testid="stSidebar"] div[data-testid="stPageLink"] a:hover,
.stSidebar div[data-testid="stPageLink"] a:hover {
    background: rgba(255, 255, 255, 0.16) !important;
    transform: translateX(3px);
}
section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"],
.stSidebar div[data-testid="stPageLink"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.96) !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.25) !important;
}
section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] *,
.stSidebar div[data-testid="stPageLink"] a[aria-current="page"] * {
    color: #5b21b6 !important;
}

.bv-side-foot {
    margin: 20px 8px 6px 8px; font-size: 0.72rem; opacity: 0.55; line-height: 1.5;
}

/* ---------- Brand mark (animated bars via CSS) ---------- */
.bv-mark {
    width: 44px; height: 44px; border-radius: 13px; flex-shrink: 0;
    display: inline-flex; align-items: center; justify-content: center; gap: 3px;
    background: var(--bv-grad);
    box-shadow: 0 10px 24px rgba(124, 58, 237, 0.4);
}
.bv-mark-bar {
    width: 4px; border-radius: 99px; background: #fff;
    animation: bvpulse 1.3s ease-in-out infinite;
}
.bv-b1 { height: 12px; animation-delay: 0s; }
.bv-b2 { height: 22px; animation-delay: 0.15s; }
.bv-b3 { height: 16px; animation-delay: 0.3s; }
.bv-b4 { height: 10px; animation-delay: 0.45s; }
@keyframes bvpulse { 0%, 100% { transform: scaleY(0.6); opacity: 0.7; } 50% { transform: scaleY(1.15); opacity: 1; } }

/* ---------- Top bar ---------- */
.st-key-topbar { margin-bottom: 26px; }
.bv-brand { display: flex; align-items: center; gap: 13px; }

/* ---------- Top navigation ---------- */
.st-key-topnav { margin-top: 14px; border-bottom: 1px solid var(--bv-border); padding-bottom: 12px; }
.st-key-topnav div[data-testid="stHorizontalBlock"],
.st-key-topnav .stHorizontalBlock { gap: 8px; }
.st-key-topnav div[data-testid="stPageLink"] a {
    background: var(--bv-soft) !important; border: 1px solid var(--bv-border) !important;
    border-radius: 12px !important; padding: 9px 14px !important; width: 100% !important;
    justify-content: center !important; font-weight: 700 !important; color: var(--bv-purple) !important;
    transition: all 0.18s ease !important;
}
.st-key-topnav div[data-testid="stPageLink"] a:hover {
    background: #ede9fe !important; transform: translateY(-1px);
}
.st-key-topnav div[data-testid="stPageLink"] a[aria-current="page"] {
    background: var(--bv-grad) !important; border-color: transparent !important;
    box-shadow: 0 8px 22px rgba(124, 58, 237, 0.30) !important;
}
.st-key-topnav div[data-testid="stPageLink"] a[aria-current="page"] * { color: #fff !important; }
.bv-brand-name { font-size: 1.35rem; font-weight: 800; white-space: nowrap; letter-spacing: -0.01em; }
.bv-brand-name .accent {
    background: var(--bv-grad); -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}
.bv-brand-tag {
    margin-left: auto; font-size: 0.72rem; font-weight: 700; color: var(--bv-purple);
    background: var(--bv-soft); border: 1px solid var(--bv-border);
    padding: 5px 12px; border-radius: 999px; letter-spacing: 0.03em;
}

/* ---------- Hero ---------- */
.bv-eyebrow {
    display: inline-block; font-size: 0.74rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--bv-purple);
    background: var(--bv-soft); border: 1px solid var(--bv-border);
    padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}
.bv-hero-title {
    font-size: 3rem; font-weight: 800; letter-spacing: -0.035em; line-height: 1.08; margin-bottom: 14px;
}
.bv-hero-title .grad {
    background: var(--bv-grad); -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}
.bv-hero-sub { font-size: 1.08rem; color: var(--bv-muted); max-width: 680px; line-height: 1.65; margin-bottom: 36px; }

/* ---------- Section headings ---------- */
.bv-kicker {
    font-size: 0.76rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--bv-purple); margin: 46px 0 6px 2px;
}
.bv-h2 { font-size: 1.7rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 22px; }

/* ---------- Generic cards ---------- */
.bv-card {
    background: var(--bv-card); border: 1px solid var(--bv-border); border-radius: var(--bv-radius);
    padding: 26px 24px; height: 100%;
    box-shadow: 0 10px 30px -22px rgba(79, 70, 229, 0.5);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}
.bv-card:hover { transform: translateY(-4px); box-shadow: var(--bv-shadow); border-color: rgba(124, 58, 237, 0.35); }

.bv-icon {
    width: 54px; height: 54px; border-radius: 16px; display: inline-flex;
    align-items: center; justify-content: center; margin-bottom: 16px;
    box-shadow: 0 10px 22px -6px rgba(124, 58, 237, 0.55);
}
.bv-icon-1 { background: linear-gradient(135deg, #6366f1, #4338ca); }
.bv-icon-2 { background: linear-gradient(135deg, #db2777, #9d174d); }

.bv-card-title { font-size: 1.22rem; font-weight: 800; margin-bottom: 7px; letter-spacing: -0.01em; }
.bv-card-desc { font-size: 0.94rem; color: var(--bv-muted); line-height: 1.6; margin-bottom: 16px; }
.bv-card-link {
    display: inline-flex; align-items: center; gap: 7px; text-decoration: none !important;
    font-weight: 700; font-size: 0.92rem; color: var(--bv-purple) !important;
}
.bv-card-link .arrow { transition: transform 0.18s ease; }
.bv-card:hover .bv-card-link .arrow { transform: translateX(4px); }

/* ---------- How to use ---------- */
.bv-step {
    background: var(--bv-card); border: 1px solid var(--bv-border); border-radius: 18px;
    padding: 22px 20px; height: 100%;
    box-shadow: 0 10px 28px -24px rgba(79, 70, 229, 0.6);
}
.bv-step-num {
    width: 38px; height: 38px; border-radius: 11px; display: inline-flex;
    align-items: center; justify-content: center; font-weight: 800; font-size: 1.05rem;
    color: #fff; background: var(--bv-grad); margin-bottom: 13px;
}
.bv-step-title { font-weight: 700; font-size: 1.02rem; margin-bottom: 5px; }
.bv-step-desc { font-size: 0.88rem; color: var(--bv-muted); line-height: 1.55; }

/* ---------- Coming soon ---------- */
.bv-soon {
    position: relative; background: linear-gradient(160deg, #faf8ff, #f3eeff);
    border: 1px dashed rgba(124, 58, 237, 0.32); border-radius: 18px;
    padding: 22px 20px; height: 100%;
}
.bv-soon-badge {
    position: absolute; top: 16px; right: 16px; font-size: 0.64rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase; color: #fff;
    background: var(--bv-grad); padding: 4px 10px; border-radius: 999px;
}
.bv-soon-emoji { font-size: 1.7rem; }
.bv-soon-title { font-weight: 700; font-size: 1.02rem; margin: 10px 0 5px 0; }
.bv-soon-desc { font-size: 0.86rem; color: var(--bv-muted); line-height: 1.55; }

/* ---------- Footer ---------- */
.bv-footer {
    margin-top: 56px; padding-top: 22px; border-top: 1px solid var(--bv-border);
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
    font-size: 0.85rem; color: var(--bv-muted);
}
.bv-footer .dot { color: var(--bv-purple); }

/* ---------- Page cards (input / result) ---------- */
.st-key-input_card, .st-key-result_card {
    background: var(--bv-card); border: 1px solid var(--bv-border); border-radius: var(--bv-radius);
    padding: 26px 28px 10px 28px; margin-bottom: 22px;
    box-shadow: 0 14px 36px -26px rgba(79, 70, 229, 0.55);
}
.st-key-input_card > div, .st-key-result_card > div { gap: 0 !important; }

.bv-section-title { font-size: 1.18rem; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.01em; }
.bv-section-caption { font-size: 0.86rem; color: var(--bv-muted); margin-bottom: 18px; }

/* ---------- Text area ---------- */
div[data-testid="stTextArea"] textarea,
.stTextArea textarea {
    border-radius: 14px !important; border: 1.5px solid var(--bv-border) !important;
    font-size: 1.02rem !important; background: #fcfbff !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
div[data-testid="stTextArea"] textarea:focus,
.stTextArea textarea:focus {
    border-color: var(--bv-purple) !important;
    box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.14) !important;
}

/* ---------- Pill script switch ---------- */
.st-key-script_switch {
    max-width: 340px; margin: 0 auto 22px auto; background: var(--bv-soft);
    border: 1px solid var(--bv-border); border-radius: 999px; padding: 5px;
}
.st-key-script_switch div[data-testid="stHorizontalBlock"],
.st-key-script_switch .stHorizontalBlock { gap: 5px; }
.st-key-script_switch button {
    border-radius: 999px !important; font-weight: 700 !important; border: none !important;
    transition: all 0.16s ease;
}
.st-key-script_switch button[kind="primary"] {
    background: var(--bv-grad) !important; color: #fff !important;
    box-shadow: 0 6px 14px rgba(124, 58, 237, 0.35) !important;
}
.st-key-script_switch button[kind="secondary"] {
    background: transparent !important; color: var(--bv-muted) !important; box-shadow: none !important;
}
.st-key-script_switch button[kind="secondary"]:hover { color: var(--bv-purple) !important; }

/* ---------- Buttons ---------- */
div[data-testid="stButton"] button[kind="primary"],
.stButton button[kind="primary"] {
    background: var(--bv-grad); border: none; border-radius: 13px; padding: 0.7rem 1.4rem;
    font-weight: 700; box-shadow: 0 10px 22px -8px rgba(124, 58, 237, 0.6);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
div[data-testid="stButton"] button[kind="primary"]:hover,
.stButton button[kind="primary"]:hover { transform: translateY(-2px); filter: brightness(1.05); }
div[data-testid="stButton"] button[kind="primary"]:active,
.stButton button[kind="primary"]:active { transform: translateY(0); }

.st-key-btn_clear button {
    border-radius: 13px !important; font-weight: 700 !important;
    border: 1.5px solid var(--bv-border) !important; color: var(--bv-purple) !important;
    background: #fff !important;
}
.st-key-btn_clear button:hover { background: var(--bv-soft) !important; }

/* ---------- Download buttons ---------- */
div[data-testid="stDownloadButton"] button,
.stDownloadButton button {
    border-radius: 13px !important; font-weight: 700 !important;
    border: 1.5px solid var(--bv-border) !important; color: var(--bv-purple) !important;
    background: #fff !important; transition: all 0.15s ease;
}
div[data-testid="stDownloadButton"] button:hover,
.stDownloadButton button:hover { background: var(--bv-soft) !important; transform: translateY(-1px); }

/* ---------- Result text ---------- */
.bv-result-text {
    border: 1px solid var(--bv-border); border-radius: 14px; padding: 18px 20px;
    min-height: 104px; font-size: 1.15rem; line-height: 1.75;
    background: linear-gradient(160deg, #faf8ff, #f5f1ff); margin-bottom: 16px;
}
.bv-avg-rating { font-size: 0.84rem; color: var(--bv-muted); margin-top: 8px; }

audio { width: 100% !important; border-radius: 12px; }

/* ---------- Mobile ---------- */
@media screen and (max-width: 640px) {
    .block-container, .stMainBlockContainer { padding-left: 1rem; padding-right: 1rem; padding-top: 2.2rem; }
    .bv-hero-title { font-size: 2.1rem; }
    .bv-hero-sub { font-size: 0.96rem; margin-bottom: 26px; }
    .bv-h2 { font-size: 1.4rem; }
    .bv-card, .bv-step, .bv-soon { margin-bottom: 16px; }
    .st-key-input_card, .st-key-result_card { padding: 20px 18px 8px 18px; }
    .st-key-script_switch { max-width: 100%; width: 100%; }
    .st-key-script_switch div[data-testid="column"],
    .st-key-script_switch .stColumn { width: 50% !important; flex: 1 1 0 !important; min-width: 0 !important; }
    .st-key-script_switch button { width: 100% !important; min-height: 42px; font-size: 0.9rem !important; }
    .bv-footer { flex-direction: column; align-items: flex-start; }
}
</style>
"""

# ----------------------------------------------------------------------------
# LAYOUT HELPERS
# ----------------------------------------------------------------------------


def inject_theme() -> None:
    """Inject the shared theme CSS. Call once per page after set_page_config."""
    # Load fonts via <link> tags first (more reliable than @import inside <style>)
    st.markdown(FONTS_LINK, unsafe_allow_html=True)
    # Then inject the theme CSS
    st.markdown(THEME_CSS, unsafe_allow_html=True)


def render_sidebar() -> None:
    """Render the branded sidebar with navigation."""
    with st.sidebar:
        st.markdown(
            f'<div class="bv-side-brand">{BRAND_MARK}'
            f'<span class="bv-side-title">Bakhteyar-AI</span></div>'
            f'<div class="bv-side-sub">Balochi Language Tools</div>',
            unsafe_allow_html=True,
        )

        st.page_link("app.py", label="Home", icon="\U0001f3e0")
        st.page_link("pages/1_\U0001f310_Translation.py", label="Translation", icon="\U0001f310")
        st.page_link("pages/2_\U0001f50a_Text_to_Speech.py", label="Text to Speech", icon="\U0001f50a")

        st.markdown(
            f'<div class="bv-side-foot">© {datetime.now().year} Bakhteyar-AI. All rights reserved.</div>',
            unsafe_allow_html=True,
        )


def render_topbar(suffix: str = "") -> None:
    """Render the top brand bar with inline navigation."""
    tag = f'<span class="bv-brand-tag">{suffix}</span>' if suffix else ""
    with st.container(key="topbar"):
        st.markdown(
            f'<div class="bv-brand">{BRAND_MARK}'
            f'<span class="bv-brand-name">Bakhteyar<span class="accent">-AI</span></span>'
            f"{tag}</div>",
            unsafe_allow_html=True,
        )
    with st.container(key="topnav"):
        cols = st.columns(3)
        with cols[0]:
            st.page_link("app.py", label="Home", icon="\U0001f3e0")
        with cols[1]:
            st.page_link("pages/1_\U0001f310_Translation.py", label="Translation", icon="\U0001f310")
        with cols[2]:
            st.page_link("pages/2_\U0001f50a_Text_to_Speech.py", label="Text to Speech", icon="\U0001f50a")


def render_footer() -> None:
    """Render the copyright footer."""
    year = datetime.now().year
    st.markdown(
        f'<div class="bv-footer">'
        f"<span>© {year} Bakhteyar-AI. All rights reserved.</span>"
        f'<span>Built for the Balochi language <span class="dot">●</span> Latin &amp; Arabic script</span>'
        f"</div>",
        unsafe_allow_html=True,
    )
