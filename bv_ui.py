
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
    '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M5 8H14M9 5V8M11 8C11 12 9 15 6 17M8 13C9 14.5 11 16 13 17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<path d="M13 20L16 11L19 20M14.5 17H17.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="18" cy="6" r="3" stroke="#db2777" stroke-width="1.5"/>'
    '</svg>'
)
 
TTS_ICON = (
    '<svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M11 5L6 9H3V15H6L11 19V5Z" fill="currentColor"/>'
    '<path d="M15.5 8.5C16.3 9.5 16.8 10.7 16.8 12C16.8 13.3 16.3 14.5 15.5 15.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M19 5C20.8 7 21.8 9.4 21.8 12C21.8 14.6 20.8 17 19 19" stroke="#db2777" stroke-width="2" stroke-linecap="round"/>'
    '</svg>'
)
 
ASR_ICON = (
    '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<path d="M12 3V14M12 3C10.5 3 9 4.5 9 6V11C9 12.5 10.5 14 12 14C13.5 14 15 12.5 15 11V6C15 4.5 13.5 3 12 3Z" stroke="url(#ai_grad)" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M19 10C19 14 15.866 17 12 17C8.134 17 5 14 5 10" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round" opacity="0.8"/>'
    '<path d="M12 17V21M9 21H15" stroke="#8b5cf6" stroke-width="2" stroke-linecap="round" opacity="0.8"/>'
    '<path d="M18 4L20 6M20 4L18 6" stroke="#db2777" stroke-width="2" stroke-linecap="round"/>'
    '<defs><linearGradient id="ai_grad" x1="9" y1="3" x2="15" y2="14" gradientUnits="userSpaceOnUse"><stop stop-color="#7c3aed"/><stop offset="1" stop-color="#db2777"/></linearGradient></defs>'
    "</svg>"
)
 
OCR_ICON = (
    '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<rect x="4" y="4" width="16" height="16" rx="3" stroke="#8b5cf6" stroke-width="2" opacity="0.6"/>'
    '<path d="M8 8H11M8 12H16M8 16H13" stroke="url(#ai_grad2)" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M16 4L18 2M14 2L16 4" stroke="#7c3aed" stroke-width="1.5" stroke-linecap="round"/>'
    '<defs><linearGradient id="ai_grad2" x1="8" y1="8" x2="16" y2="16" gradientUnits="userSpaceOnUse"><stop stop-color="#7c3aed"/><stop offset="1" stop-color="#db2777"/></linearGradient></defs>'
    "</svg>"
)
 
DATA_ICON = (
    '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">'
    '<ellipse cx="12" cy="6" rx="8" ry="3" stroke="#8b5cf6" stroke-width="2" opacity="0.6"/>'
    '<path d="M4 6V18C4 19.6569 7.58172 21 12 21C16.4183 21 20 19.6569 20 18V6" stroke="#8b5cf6" stroke-width="2" opacity="0.6"/>'
    '<path d="M4 12C4 13.6569 7.58172 15 12 15C16.4183 15 20 13.6569 20 12" stroke="url(#ai_grad3)" stroke-width="2"/>'
    '<path d="M14 18L16 20L20 16" stroke="#db2777" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    '<defs><linearGradient id="ai_grad3" x1="4" y1="12" x2="20" y2="15" gradientUnits="userSpaceOnUse"><stop stop-color="#7c3aed"/><stop offset="1" stop-color="#db2777"/></linearGradient></defs>'
    "</svg>"
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
        "sidebar_bg": "#f8f9fa",
        "sidebar_text": "#1e1b2e",
        "input_bg": "#ffffff",
        "font_main": "'Inter', sans-serif",
        "toggle_btn_bg": "#7c3aed",
        "toggle_btn_text": "#ffffff",
        "toggle_btn_border": "#7c3aed",
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
        "sidebar_bg": "#0f0e16",
        "sidebar_text": "#ffffff",
        "input_bg": "#1e1b2e",
        "font_main": "'Sora', sans-serif",
        "toggle_btn_bg": "#ffffff",
        "toggle_btn_text": "#7c3aed",
        "toggle_btn_border": "#ffffff",
    }
}
 
# ----------------------------------------------------------------------------
# THEME CSS
# ----------------------------------------------------------------------------
 
THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Sora:wght@600;700;800&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap');
 
:root {{
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
    --bv-input-bg: {input_bg};
}}
 
html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {{
    font-family: {font_main}, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--bv-ink);
}}
 
/* Soft ambient background glow */
[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(900px 500px at 12% -10%, {bg_glow_1}, transparent 60%),
        radial-gradient(800px 500px at 100% 0%, {bg_glow_2}, transparent 55%),
        {bg};
}}
 
#MainMenu, footer {{ visibility: hidden; }}
header[data-testid="stHeader"] {{ background: transparent !important; }}
 
.block-container {{
    padding-top: 2.6rem;
    padding-bottom: 3rem;
    max-width: 940px;
}}
 
h1, h2, h3, .bv-hero-title, .bv-brand-name, .bv-side-title {{
    font-family: 'Sora', 'Inter', sans-serif;
}}
 
/* ---------- Hide default sidebar nav ---------- */
[data-testid="stSidebarNav"] {{ display: none !important; }}
 
/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {{
    background: {sidebar_bg} !important;
    border-right: 1px solid var(--bv-border) !important;
}}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] .bv-side-title,
[data-testid="stSidebar"] .bv-side-sub,
[data-testid="stSidebar"] .bv-side-foot {{ 
    color: {sidebar_text} !important; 
    opacity: 1.0 !important;
}}

/* Sidebar Toggle Button Visibility Fix */
button[data-testid="stSidebarCollapse"] {{
    color: {sidebar_text} !important;
    background-color: transparent !important;
    border: none !important;
    width: 40px !important;
    height: 40px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    z-index: 999999 !important;
}}
button[data-testid="stSidebarCollapse"] svg {{
    fill: {sidebar_text} !important;
    width: 24px !important;
    height: 24px !important;
}}

/* Theme Toggle Specific Styling */
.st-key-theme_toggle button {{
    background: {toggle_btn_bg} !important;
    color: {toggle_btn_text} !important;
    border: 2px solid {toggle_btn_border} !important;
    border-radius: 999px !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}}
.st-key-theme_toggle button p {{
    color: {toggle_btn_text} !important;
    font-weight: 800 !important;
}}
.st-key-theme_toggle button:hover {{
    transform: scale(1.02);
    opacity: 0.9;
}}
 
div[data-testid="stSidebarUserContent"] {{ padding-top: 1rem; }}
 
.bv-side-brand {{
    display: flex; align-items: center; gap: 12px;
    padding: 6px 6px 4px 6px;
}}
.bv-side-title {{ font-size: 1.25rem; font-weight: 800; line-height: 1; }}
.bv-side-sub {{ font-size: 0.78rem; opacity: 0.8; margin: 14px 6px 10px 6px; letter-spacing: 0.04em; text-transform: uppercase; }}
 
[data-testid="stSidebar"] div[data-testid="stPageLink"] a {{
    background: rgba(124, 58, 237, 0.05) !important;
    border: 1px solid var(--bv-border) !important;
    border-radius: 14px !important;
    margin: 7px 4px !important;
    padding: 11px 14px !important;
    font-weight: 600 !important;
    color: {sidebar_text} !important;
    justify-content: flex-start !important;
    transition: all 0.18s ease !important;
}}
[data-testid="stSidebar"] div[data-testid="stPageLink"] a:hover {{
    background: rgba(124, 58, 237, 0.12) !important;
    transform: translateX(3px);
}}
[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] {{
    background: var(--bv-grad) !important;
    border: none !important;
    box-shadow: 0 8px 22px rgba(124, 58, 237, 0.25) !important;
}}
[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] * {{
    color: white !important;
}}
 
.bv-side-foot {{
    margin: 20px 8px 6px 8px; font-size: 0.72rem; opacity: 0.8 !important; line-height: 1.5;
}}
 
/* ---------- Brand mark (animated bars) ---------- */
.bv-mark {{
    width: 44px; height: 44px; border-radius: 13px; flex-shrink: 0;
    display: inline-flex; align-items: center; justify-content: center; gap: 3px;
    background: var(--bv-grad);
    box-shadow: 0 10px 24px rgba(124, 58, 237, 0.4);
}}
.bv-mark-bar {{
    width: 4px; border-radius: 99px; background: #fff;
    animation: bvpulse 1.3s ease-in-out infinite;
}}
.bv-b1 {{ height: 12px; animation-delay: 0s; }}
.bv-b2 {{ height: 22px; animation-delay: 0.15s; }}
.bv-b3 {{ height: 16px; animation-delay: 0.3s; }}
.bv-b4 {{ height: 10px; animation-delay: 0.45s; }}
@keyframes bvpulse {{ 0%, 100% {{ transform: scaleY(0.6); opacity: 0.7; }} 50% {{ transform: scaleY(1.15); opacity: 1; }} }}
 
/* ---------- Top bar ---------- */
.st-key-topbar {{ margin-bottom: 26px; }}
.bv-brand {{ display: flex; align-items: center; gap: 13px; }}
 
/* ---------- Top navigation (removed) ---------- */
.bv-brand-name {{ font-size: 1.35rem; font-weight: 800; white-space: nowrap; letter-spacing: -0.01em; margin-top: -2px; }}
.bv-brand-name .accent {{
    background: var(--bv-grad); -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.bv-brand-tag {{
    margin-left: auto; font-size: 0.72rem; font-weight: 700; color: var(--bv-purple);
    background: var(--bv-soft); border: 1px solid var(--bv-border);
    padding: 5px 12px; border-radius: 999px; letter-spacing: 0.03em;
}}
 
/* ---------- Hero ---------- */
.bv-eyebrow {{
    display: inline-block; font-size: 0.74rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: var(--bv-purple);
    background: var(--bv-soft); border: 1px solid var(--bv-border);
    padding: 6px 14px; border-radius: 999px; margin-bottom: 16px;
}}
.bv-hero-title {{
    font-size: 3rem; font-weight: 800; letter-spacing: -0.035em; line-height: 1.08; margin-bottom: 14px;
}}
.bv-hero-title .grad {{
    background: var(--bv-grad); -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent;
}}
.bv-hero-sub {{ font-size: 1.08rem; color: var(--bv-muted); max-width: 680px; line-height: 1.65; margin-bottom: 36px; }}
 
/* ---------- Section headings ---------- */
.bv-kicker {{
    font-size: 0.76rem; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
    color: var(--bv-purple); margin: 46px 0 6px 2px;
}}
.bv-h2 {{ font-size: 1.7rem; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 22px; }}
 
/* ---------- Generic cards ---------- */
.bv-card {{
    background: var(--bv-card); border: 1px solid var(--bv-border); border-radius: var(--bv-radius);
    padding: 26px 24px; height: 100%;
    box-shadow: 0 10px 30px -22px rgba(79, 70, 229, 0.5);
    transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
}}
.bv-card:hover {{ transform: translateY(-4px); box-shadow: var(--bv-shadow); border-color: rgba(124, 58, 237, 0.35); }}
 
.bv-icon {{
    width: 54px; height: 54px; border-radius: 16px; display: inline-flex;
    align-items: center; justify-content: center; margin-bottom: 16px;
    box-shadow: 0 10px 22px -6px rgba(124, 58, 237, 0.55);
    color: white !important;
}}
.bv-icon-1 {{ background: linear-gradient(135deg, #6366f1, #4338ca); }}
.bv-icon-2 {{ background: linear-gradient(135deg, #db2777, #9d174d); }}
 
.bv-card-title {{ font-size: 1.22rem; font-weight: 800; margin-bottom: 7px; letter-spacing: -0.01em; }}
.bv-card-desc {{ font-size: 0.94rem; color: var(--bv-muted); line-height: 1.6; margin-bottom: 16px; }}
.bv-card-link {{
    display: inline-flex; align-items: center; gap: 7px; text-decoration: none !important;
    font-weight: 700; font-size: 0.92rem; color: var(--bv-purple) !important;
}}
.bv-card-link .arrow {{ transition: transform 0.18s ease; }}
.bv-card:hover .bv-card-link .arrow {{ transform: translateX(4px); }}
 
/* ---------- How to use ---------- */
.bv-step {{
    background: var(--bv-card); border: 1px solid var(--bv-border); border-radius: 18px;
    padding: 22px 20px; height: 100%;
    box-shadow: 0 10px 28px -24px rgba(79, 70, 229, 0.6);
}}
.bv-step-num {{
    width: 38px; height: 38px; border-radius: 11px; display: inline-flex;
    align-items: center; justify-content: center; font-weight: 800; font-size: 1.05rem;
    color: #fff; background: var(--bv-grad); margin-bottom: 13px;
}}
.bv-step-title {{ font-weight: 700; font-size: 1.02rem; margin-bottom: 5px; }}
.bv-step-desc {{ font-size: 0.88rem; color: var(--bv-muted); line-height: 1.55; }}
 
/* ---------- Coming soon ---------- */
.bv-soon {{
    position: relative; background: var(--bv-soft);
    border: 1px dashed var(--bv-border); border-radius: 18px;
    padding: 22px 20px; height: 100%;
}}
.bv-soon-badge {{
    position: absolute; top: 16px; right: 16px; font-size: 0.64rem; font-weight: 800;
    letter-spacing: 0.08em; text-transform: uppercase; color: #fff;
    background: var(--bv-grad); padding: 4px 10px; border-radius: 999px;
}}
.bv-soon-emoji {{ 
    font-size: 1.7rem; 
    color: var(--bv-purple);
    display: flex;
    align-items: center;
}}
.bv-soon-title {{ font-weight: 700; font-size: 1.02rem; margin: 10px 0 5px 0; }}
.bv-soon-desc {{ font-size: 0.86rem; color: var(--bv-muted); line-height: 1.55; }}
 
/* ---------- Footer ---------- */
.bv-footer {{
    margin-top: 56px; padding-top: 22px; border-top: 1px solid var(--bv-border);
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
    font-size: 0.85rem; color: var(--bv-muted);
}}
.bv-footer .dot {{ color: var(--bv-purple); }}
 
/* ---------- Page cards (input / result) ---------- */
.st-key-input_card, .st-key-result_card {{
    background: var(--bv-card); border: 1px solid var(--bv-border); border-radius: var(--bv-radius);
    padding: 26px 28px 24px 28px; margin-bottom: 22px;
    box-shadow: 0 14px 36px -26px rgba(79, 70, 229, 0.55);
}}
.st-key-input_card > div, .st-key-result_card > div {{ gap: 0.8rem !important; }}
 
.bv-section-title {{ font-size: 1.18rem; font-weight: 800; margin-bottom: 4px; letter-spacing: -0.01em; }}
.bv-section-caption {{ font-size: 0.86rem; color: var(--bv-muted); margin-bottom: 18px; }}
 
/* ---------- Text area ---------- */
div[data-testid="stTextArea"] textarea {{
    border-radius: 14px !important; border: 1.5px solid var(--bv-border) !important;
    font-size: 1.02rem !important; background: var(--bv-input-bg) !important;
    color: var(--bv-ink) !important;
    caret-color: #7c3aed !important;
    transition: border-color 0.15s ease, box-shadow 0.15s ease;
}}
div[data-testid="stTextArea"] textarea::placeholder {{
    color: var(--bv-muted) !important;
    opacity: 0.7 !important;
}}
div[data-testid="stTextArea"] textarea:focus {{
    border-color: var(--bv-purple) !important;
    box-shadow: 0 0 0 4px rgba(124, 58, 237, 0.14) !important;
}}
 
/* ---------- Pill script switch ---------- */
.st-key-script_switch {{
    max-width: 340px; margin: 0 auto 22px auto; background: var(--bv-soft);
    border: 1px solid var(--bv-border); border-radius: 999px; padding: 5px;
}}
.st-key-script_switch div[data-testid="stHorizontalBlock"] {{ gap: 5px; }}
.st-key-script_switch button {{
    border-radius: 999px !important; font-weight: 700 !important; border: none !important;
    transition: all 0.16s ease;
}}
.st-key-script_switch button[kind="primary"] {{
    background: var(--bv-grad) !important; color: #fff !important;
    box-shadow: 0 6px 14px rgba(124, 58, 237, 0.35) !important;
}}
.st-key-script_switch button[kind="secondary"] {{
    background: transparent !important; color: {ink} !important; opacity: 0.6 !important; box-shadow: none !important;
}}
.st-key-script_switch button[kind="secondary"]:hover {{ color: var(--bv-purple) !important; opacity: 1 !important; }}
 
/* ---------- Buttons ---------- */
div[data-testid="stButton"] button[kind="primary"], 
div[data-testid="stButton"] button[data-testid="baseButton-primary"] {{
    background: var(--bv-grad); border: none; border-radius: 13px; padding: 0.7rem 1.4rem;
    font-weight: 700; box-shadow: 0 10px 22px -8px rgba(124, 58, 237, 0.6);
    transition: transform 0.15s ease, box-shadow 0.15s ease, filter 0.15s ease;
}}
div[data-testid="stButton"] button[kind="primary"]:hover,
div[data-testid="stButton"] button[data-testid="baseButton-primary"]:hover {{ transform: translateY(-2px); filter: brightness(1.05); }}
div[data-testid="stButton"] button[kind="primary"]:active,
div[data-testid="stButton"] button[data-testid="baseButton-primary"]:active {{ transform: translateY(0); }}
 
.st-key-btn_clear button {{
    border-radius: 13px !important; font-weight: 700 !important;
    border: 1.5px solid var(--bv-border) !important; color: var(--bv-purple) !important;
    background: var(--bv-input-bg) !important;
}}
 
/* ---------- Audio Player ---------- */
audio {{ width: 100%; border-radius: 14px; margin-bottom: 12px; }}
 
/* ---------- Rating Feedback ---------- */
.bv-avg-rating {{
    font-size: 0.8rem; color: var(--bv-muted); margin-top: 10px; text-align: center;
}}
 
/* ---------- Result Text Display ---------- */
.bv-result-text {{
    padding: 22px; border-radius: 16px; background: var(--bv-soft);
    border: 1.5px solid var(--bv-border); font-size: 1.25rem; line-height: 1.6;
    margin-bottom: 18px; min-height: 80px;
}}
 
/* ---------- Responsive Grid Fixes ---------- */
@media screen and (max-width: 640px) {{
    .bv-hero-title {{ font-size: 2.2rem; }}
    .st-key-input_card, .st-key-result_card {{ padding: 18px 16px; }}
}}
</style>
"""
 
 
def inject_theme():
    mode = st.session_state.get("theme_mode", "light")
    config = THEME_CONFIG[mode]
    st.markdown(THEME_CSS.format(**config), unsafe_allow_html=True)
 
 
def render_sidebar():
    with st.sidebar:
        st.markdown(
            f"""
            <div class="bv-side-brand">
                {BRAND_MARK}
                <div class="bv-side-title">Bakhteyar AI</div>
            </div>
            <div class="bv-side-sub">Tools & Navigation</div>
            """,
            unsafe_allow_html=True,
        )
 
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_🌐_Translation.py", label="Translate", icon="🌐")
        st.page_link("pages/2_🔊_Text_to_Speech.py", label="Voice", icon="🎙️")
 
        st.markdown('<div class="bv-side-sub">Preferences</div>', unsafe_allow_html=True)
        
        mode = st.session_state.get("theme_mode", "light")
        new_mode = "dark" if mode == "light" else "light"
        btn_label = "🌙 Dark Mode" if mode == "light" else "☀️ Light Mode"
        
        if st.button(btn_label, key="theme_toggle", use_container_width=True):
            st.session_state.theme_mode = new_mode
            st.rerun()
 
        st.markdown(
            f"""
            <div class="bv-side-foot">
                &copy; {datetime.now().year} Bakhteyar-AI<br/>
                Fine-tuned models for Balochi.
            </div>
            """,
            unsafe_allow_html=True,
        )
 
 
def render_topbar(current_page: str = None):
    cols = st.columns([1, 1])
    with cols[0]:
        st.markdown(
            f"""
            <div class="bv-brand">
                <div class="bv-brand-name">Bakhteyar<span class="accent">AI</span></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with cols[1]:
        if current_page:
            st.markdown(f'<div class="bv-brand-tag">{current_page}</div>', unsafe_allow_html=True)
 
 
def render_footer():
    st.markdown(
        f"""
        <div class="bv-footer">
            <div>Built for the <b>Balochi</b> community <span class="dot">&bull;</span> {datetime.now().year}</div>
            <div>Bakhteyar-AI v1.0</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
