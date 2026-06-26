
"""Shared UI theme, branding and layout helpers for the Bakhteyar-AI Streamlit app.
 
Keeping the CSS and the sidebar / top-bar / footer markup in one place keeps the
three pages consistent and makes the design easy to tweak in a single spot.
"""
 
from datetime import datetime
 
import streamlit as st
 
# ----------------------------------------------------------------------------
# BRAND MARKS (pure CSS / inline SVG so there are no image assets to ship)
# ----------------------------------------------------------------------------
 
BRAND_MARK = (
    '<span class="bv-mark">'
    '<span class="bv-mark-bar bv-b1"></span>'
    '<span class="bv-mark-bar bv-b2"></span>'
    '<span class="bv-mark-bar bv-b3"></span>'
    '<span class="bv-mark-bar bv-b4"></span>'
    "</span>"
)
 
TRANSLATION_ICON = (
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M4 5h8M8 3v2M9.5 5c0 3.5-2 6.5-5.5 8M6 9c1.2 2 3 3.5 5 4.2" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M13 21l4-9 4 9M14.5 18h5" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)
 
TTS_ICON = (
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M11 5L6 9H3v6h3l5 4V5z" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M15.5 8.5a5 5 0 010 7M18.5 6a8.5 8.5 0 010 12" stroke="white" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'
    "</svg>"
)

ASR_ICON = (
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z"/>'
    '<path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" x2="12" y1="19" y2="22"/></svg>'
)

OCR_ICON = (
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M3 7V5a2 2 0 0 1 2-2h2"/><path d="M17 3h2a2 2 0 0 1 2 2v2"/><path d="M21 17v2a2 2 0 0 1-2 2h-2"/><path d="M7 21H5a2 2 0 0 1-2-2v-2"/>'
    '<path d="M7 8h10"/><path d="M7 12h10"/><path d="M7 16h10"/></svg>'
)

DATA_ICON = (
    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
    '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5V19A9 3 0 0 0 21 19V5"/><path d="M3 12A9 3 0 0 0 21 12"/></svg>'
)

# ----------------------------------------------------------------------------
# THEME CONFIG
# ----------------------------------------------------------------------------

THEME_CONFIG = {
    "light": {
        "ink": "#1e1b2e",
        "muted": "#6b6783",
        "border": "rgba(124, 58, 237, 0.14)",
        "card": "#ffffff",
        "soft": "#f5f3ff",
        "bg": "#ffffff",
        "bg_glow_1": "rgba(124, 58, 237, 0.10)",
        "bg_glow_2": "rgba(219, 39, 119, 0.08)",
    },
    "dark": {
        "ink": "#f3f0ff",
        "muted": "#9d99b9",
        "border": "rgba(167, 139, 250, 0.2)",
        "card": "#13111c",
        "soft": "#1e1b2e",
        "bg": "#0b0a0f",
        "bg_glow_1": "rgba(124, 58, 237, 0.15)",
        "bg_glow_2": "rgba(219, 39, 119, 0.12)",
    }
}
 
# ----------------------------------------------------------------------------
# THEME CSS
# ----------------------------------------------------------------------------
 
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@600;700;800&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap');
 
:root {
    --bv-ink: {ink};
    --bv-muted: {muted};
    --bv-border: {border};
    --bv-card: {card};
    --bv-soft: {soft};
    --bv-purple: #7c3aed;
    --bv-purple-2: #6d28d9;
    --bv-indigo: #4f46e5;
    --bv-pink: #db2777;
    --bv-grad: linear-gradient(135deg, #7c3aed 0%, #6366f1 50%, #db2777 100%);
    --bv-radius: 20px;
    --bv-shadow: 0 18px 40px -18px rgba(79, 70, 229, 0.45);
}
 
html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--bv-ink);
}
 
/* Soft ambient background glow */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(900px 500px at 12% -10%, {bg_glow_1}, transparent 60%),
        radial-gradient(800px 500px at 100% 0%, {bg_glow_2}, transparent 55%),
        {bg};
}
 
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }
 
.block-container {
    padding-top: 2.6rem;
    padding-bottom: 3rem;
    max-width: 940px;
}
 
h1, h2, h3, .bv-hero-title, .bv-brand-name, .bv-side-title {
    font-family: 'Sora', 'Inter', sans-serif;
}
 
/* ---------- Hide default sidebar nav ---------- */
[data-testid="stSidebarNav"] { display: none !important; }
 
/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #2a1758 0%, #4c1d95 55%, #6d28d9 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * { color: #f3eaff !important; }
 
div[data-testid="stSidebarUserContent"] { padding-top: 1rem; }
 
.bv-side-brand {
    display: flex; align-items: center; gap: 12px;
    padding: 6px 6px 4px 6px;
}
.bv-side-title { font-size: 1.25rem; font-weight: 800; line-height: 1; }
.bv-side-sub { font-size: 0.78rem; opacity: 0.7; margin: 14px 6px 10px 6px; letter-spacing: 0.04em; text-transform: uppercase; }
 
[data-testid="stSidebar"] div[data-testid="stPageLink"] a {
    background: rgba(255, 255, 255, 0.06) !important;
    border: 1px solid rgba(255, 255, 255, 0.10) !important;
    border-radius: 14px !important;
    margin: 7px 4px !important;
    padding: 11px 14px !important;
    font-weight: 600 !important;
    justify-content: flex-start !important;
    transition: all 0.18s ease !important;
}
[data-testid="stSidebar"] div[data-testid="stPageLink"] a:hover {
    background: rgba(255, 255, 255, 0.16) !important;
    transform: translateX(3px);
}
[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.96) !important;
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.25) !important;
}
[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] * {
    color: #5b21b6 !important;
}
 
.bv-side-foot {
    margin: 20px 8px 6px 8px; font-size: 0.72rem; opacity: 0.55; line-height: 1.5;
}
 
/* ---------- Brand mark (animated bars) ---------- */
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
 
/* ---------- Top navigation (removed) ---------- */
.bv-brand-name { font-size: 1.35rem; font-weight: 800; white-space: nowrap; letter-spacing: -0.01em; margin-top: -2px; }
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
    padding: 26px 28px 24px 28px; margin-bottom: 22px;
    box-shadow: 0 14px 36px -26px rgba(79, 70, 229, 0.55);
}
.st-key-input_card > div, .st-key-result_card > div { gap: 0.8rem !important; }
 
.bv-section-title { font-size: 1.18rem; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.01em; }
.bv-section-caption { font-size: 0.86rem; color: var(--bv-muted); margin-bottom: 18px; }
 
/* ---------- Text area ---------- */
div[data-testid="stTextArea"] textarea {
    border-radius: 14px !important; border: 1.5px solid var(--bv-border) !important;
    font-size: 1.02rem !important; background: #fcfbff !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
div[data-testid="stTextArea"] textarea:focus {
    border-color: var(--bv-purple) !important;
    box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.14) !important;
}
 
/* ---------- Pill script switch ---------- */
.st-key-script_switch {
    max-width: 340px; margin: 0 auto 22px auto; background: var(--bv-soft);
    border: 1px solid var(--bv-border); border-radius: 999px; padding: 5px;
}
.st-key-script_switch div[data-testid="stHorizontalBlock"] { gap: 5px; }
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
div[data-testid="stButton"] button[data-testid="baseButton-primary"] {
    background: var(--bv-grad); border: none; border-radius: 13px; padding: 0.7rem 1.4rem;
    font-weight: 700; box-shadow: 0 10px 22px -8px rgba(124, 58, 237, 0.6);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}
div[data-testid="stButton"] button[kind="primary"]:hover,
div[data-testid="stButton"] button[data-testid="baseButton-primary"]:hover { transform: translateY(-2px); filter: brightness(1.05); }
div[data-testid="stButton"] button[kind="primary"]:active,
div[data-testid="stButton"] button[data-testid="baseButton-primary"]:active { transform: translateY(0); }
 
.st-key-btn_clear button {
    border-radius: 13px !important; font-weight: 700 !important;
    border: 1.5px solid var(--bv-border) !important; color: var(--bv-purple) !important;
    background: #fff !important;
}
.st-key-btn_clear button:hover { background: var(--bv-soft) !important; }
 
/* ---------- Download buttons ---------- */
div[data-testid="stDownloadButton"] button {
    border-radius: 13px !important; font-weight: 700 !important;
    border: 1.5px solid var(--bv-border) !important; color: var(--bv-purple) !important;
    background: #fff !important; transition: all 0.15s ease;
}
div[data-testid="stDownloadButton"] button:hover { background: var(--bv-soft) !important; transform: translateY(-1px); }
 
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
    .block-container { padding-left: 1rem; padding-right: 1rem; padding-top: 2.2rem; }
    .bv-hero-title { font-size: 2.1rem; }
    .bv-hero-sub { font-size: 0.96rem; margin-bottom: 26px; }
    .bv-h2 { font-size: 1.4rem; }
    .bv-card, .bv-step, .bv-soon { margin-bottom: 16px; }
    .st-key-input_card, .st-key-result_card { padding: 20px 18px 8px 18px; }
    .st-key-script_switch { max-width: 100%; width: 100%; }
    .st-key-script_switch div[data-testid="column"] { width: 50% !important; flex: 1 1 0 !important; min-width: 0 !important; }
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
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    cfg = THEME_CONFIG[st.session_state.theme]
    css = THEME_CSS
    for key, value in cfg.items():
        css = css.replace(f"{{{key}}}", value)
    st.markdown(css, unsafe_allow_html=True)


def render_theme_toggle() -> None:
    """Render a theme toggle button."""
    if "theme" not in st.session_state:
        st.session_state.theme = "light"
    
    label = "🌙 Dark Mode" if st.session_state.theme == "light" else "☀️ Light Mode"
    if st.button(label, use_container_width=True, key="theme_toggle"):
        st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"
        st.rerun()


def render_sidebar() -> None:
    """Render the branded sidebar with navigation."""
    with st.sidebar:
        st.markdown(
            f'<div class="bv-side-brand">{BRAND_MARK}'
            f'<div class="bv-side-title">Bakhteyar-AI</div></div>'
            f'<div class="bv-side-sub">Balochi Language Tools</div>',
            unsafe_allow_html=True,
        )
 
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_🌐_Translation.py", label="Translation", icon="🌐")
        st.page_link("pages/2_🔊_Text_to_Speech.py", label="Text to Speech", icon="🔊")

        st.markdown('<div style="margin-top: 2rem;"></div>', unsafe_allow_html=True)
        render_theme_toggle()
 
        st.markdown(
            f'<div class="bv-side-foot">© {datetime.now().year} Bakhteyar-AI.<br>All rights reserved.</div>',
            unsafe_allow_html=True,
        )
 
 
def render_topbar(suffix: str = "") -> None:
    """Render the top brand bar.
 
    The navigation is handled exclusively by the sidebar to avoid redundancy.
    """
    tag = f'<span class="bv-brand-tag">{suffix}</span>' if suffix else ""
    with st.container(key="topbar"):
        st.markdown(
            f'<div class="bv-brand">{BRAND_MARK}'
            f'<span class="bv-brand-name">Bakhteyar<span class="accent">-AI</span></span>'
            f"{tag}</div>",
            unsafe_allow_html=True,
        )
 
 
def render_footer() -> None:
    """Render the copyright footer."""
    year = datetime.now().year
    st.markdown(
        f'<div class="bv-footer">'
        f"<div>© {year} Bakhteyar-AI. All rights reserved.</div>"
        f'<div>Built for the Balochi language <span class="dot">●</span> Latin &amp; Arabic script</div>'
        f"</div>",
        unsafe_allow_html=True,
    )
