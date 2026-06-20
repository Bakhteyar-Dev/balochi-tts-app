import streamlit as st

# ----------------------------------------------------------------------------
# STYLES
# ----------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bv-ink: var(--text-color);
    --bv-muted: color-mix(in srgb, var(--text-color) 60%, transparent);
    --bv-border: color-mix(in srgb, var(--text-color) 16%, transparent);
    --bv-card-bg: var(--secondary-background-color);
    --bv-purple: #8a5cf0;
    --bv-purple-dark: #6f3fdc;
    --bv-card-radius: 16px;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    color: var(--bv-ink);
}

.block-container {
    padding-top: 3.2rem;
    max-width: 880px;
}

/* ---------- Hide default Streamlit sidebar navigation ---------- */
[data-testid="stSidebarNav"],
section[data-testid="stSidebarNav"],
div[data-testid="stSidebarNav"],
ul[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavItems"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
    overflow: hidden !important;
}

/* ---------- Custom sidebar ---------- */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fbff 0%, #eef6ff 100%) !important;
    border-right: 1px solid var(--bv-border);
}

div[data-testid="stSidebarUserContent"] {
    padding-top: 1.2rem;
}

.bv-side-title {
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 4px;
    color: #111827;
}

.bv-side-sub {
    font-size: 0.85rem;
    color: #6b7280;
    margin-bottom: 22px;
}

/* ---------- Custom sidebar coloured buttons ---------- */
section[data-testid="stSidebar"] div[data-testid="stPageLink"] a {
    background: linear-gradient(135deg, #8a5cf0, #6f3fdc) !important;
    color: white !important;
    border-radius: 14px !important;
    margin: 8px 8px !important;
    padding: 12px 14px !important;
    font-weight: 800 !important;
    justify-content: flex-start !important;
    box-shadow: 0 6px 16px rgba(111, 63, 220, 0.22) !important;
}

section[data-testid="stSidebar"] div[data-testid="stPageLink"] a p,
section[data-testid="stSidebar"] div[data-testid="stPageLink"] a span {
    color: white !important;
}

section[data-testid="stSidebar"] div[data-testid="stPageLink"] a:hover {
    opacity: 0.92 !important;
}

section[data-testid="stSidebar"] div[data-testid="stPageLink"] a[aria-current="page"] {
    background: linear-gradient(135deg, #6f3fdc, #4c1d95) !important;
    color: white !important;
}

/* ---------- Main top brand ---------- */
.bv-brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.bv-brand-name {
    font-size: 1.4rem;
    font-weight: 700;
    white-space: nowrap;
}

.bv-brand-name .accent {
    color: var(--bv-purple);
}

.st-key-topbar {
    border-bottom: 1px solid var(--bv-border);
    margin-bottom: 36px;
    padding-bottom: 14px;
}

.bv-hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 10px;
    line-height: 1.15;
}

.bv-hero-sub {
    font-size: 1.05rem;
    color: var(--bv-muted);
    max-width: 640px;
    line-height: 1.6;
    margin-bottom: 38px;
}

.bv-tool-card {
    background: var(--bv-card-bg);
    border: 1px solid var(--bv-border);
    border-radius: var(--bv-card-radius);
    padding: 26px 24px;
    height: 100%;
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.bv-tool-title {
    font-size: 1.25rem;
    font-weight: 700;
    margin-bottom: 6px;
}

.bv-tool-desc {
    font-size: 0.92rem;
    color: var(--bv-muted);
    line-height: 1.55;
    margin-bottom: 8px;
}

/* ---------- Code-made app logos ---------- */
.app-logo {
    width: 54px;
    height: 54px;
    border-radius: 17px;
    display: inline-flex;
    position: relative;
    overflow: hidden;
    flex-shrink: 0;
    box-shadow: 0 10px 24px rgba(79, 70, 229, 0.28);
}

.brand-app-logo {
    width: 38px;
    height: 38px;
    border-radius: 12px;
    box-shadow: 0 6px 18px rgba(111, 63, 220, 0.28);
}

.card-logo {
    margin-bottom: 6px;
}

/* ---------- Translation logo ---------- */
.translation-logo {
    background: radial-gradient(circle at 50% 45%, #1d4ed8 0%, #0f2e91 46%, #06164f 100%);
}

.translation-logo::before {
    content: "";
    position: absolute;
    width: 42px;
    height: 42px;
    border: 3px solid rgba(125, 211, 252, 0.85);
    border-radius: 50%;
    left: 5px;
    top: 5px;
    box-shadow: 0 0 12px rgba(125, 211, 252, 0.65);
}

.logo-bubble {
    position: absolute;
    width: 17px;
    height: 17px;
    border-radius: 5px;
    background: white;
    color: #1d4ed8 !important;
    font-size: 10px;
    font-weight: 900;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.25);
    z-index: 3;
}

.brand-app-logo .logo-bubble {
    width: 12px;
    height: 12px;
    font-size: 7px;
    border-radius: 4px;
}

.logo-a {
    left: 7px;
    top: 12px;
}

.logo-b {
    left: 18px;
    top: 27px;
    background: #2563eb;
    color: white !important;
}

.logo-c {
    right: 7px;
    top: 15px;
}

.logo-arrow {
    position: absolute;
    width: 24px;
    height: 3px;
    border-radius: 99px;
    z-index: 2;
}

.arrow-one {
    background: #22d3ee;
    left: 8px;
    bottom: 10px;
    transform: rotate(-28deg);
}

.arrow-two {
    background: #a855f7;
    right: 7px;
    top: 9px;
    transform: rotate(28deg);
}

/* ---------- Purple speech/audio logo ---------- */
.voice-logo {
    background:
        radial-gradient(circle at 48% 40%, #b26cff 0%, #7c2df0 42%, #3b087c 100%);
}

.voice-logo::before {
    content: "";
    position: absolute;
    width: 38px;
    height: 34px;
    left: 7px;
    top: 8px;
    border: 3px solid rgba(238, 215, 255, 0.9);
    border-radius: 50%;
    box-shadow:
        0 0 10px rgba(216, 180, 254, 0.75),
        inset 0 0 10px rgba(216, 180, 254, 0.25);
}

.voice-logo::after {
    content: "";
    position: absolute;
    width: 12px;
    height: 10px;
    left: 11px;
    bottom: 10px;
    border-left: 3px solid rgba(238, 215, 255, 0.95);
    border-bottom: 3px solid rgba(238, 215, 255, 0.95);
    border-radius: 0 0 0 10px;
    transform: rotate(-18deg);
    box-shadow: 0 0 8px rgba(216, 180, 254, 0.65);
}

.voice-bar {
    position: absolute;
    bottom: 14px;
    width: 7px;
    border-radius: 99px;
    background: linear-gradient(180deg, #ffffff, #d8b4fe);
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.55);
    z-index: 4;
}

.voice-bar-one {
    height: 18px;
    left: 15px;
}

.voice-bar-two {
    height: 28px;
    left: 24px;
}

.voice-bar-three {
    height: 21px;
    left: 33px;
}

.voice-wave {
    position: absolute;
    top: 24px;
    width: 12px;
    height: 3px;
    border-radius: 99px;
    background: rgba(255, 255, 255, 0.65);
    box-shadow: 0 0 8px rgba(216, 180, 254, 0.75);
    z-index: 3;
}

.voice-wave-left {
    left: 4px;
}

.voice-wave-right {
    right: 4px;
}

.brand-app-logo::before {
    width: 27px;
    height: 24px;
    left: 5px;
    top: 6px;
    border-width: 2px;
}

.brand-app-logo::after {
    width: 8px;
    height: 7px;
    left: 8px;
    bottom: 7px;
    border-left-width: 2px;
    border-bottom-width: 2px;
}

.brand-app-logo .voice-bar {
    bottom: 10px;
    width: 5px;
}

.brand-app-logo .voice-bar-one {
    height: 13px;
    left: 11px;
}

.brand-app-logo .voice-bar-two {
    height: 20px;
    left: 17px;
}

.brand-app-logo .voice-bar-three {
    height: 15px;
    left: 23px;
}

.brand-app-logo .voice-wave {
    top: 17px;
    width: 8px;
    height: 2px;
}

.brand-app-logo .voice-wave-left {
    left: 3px;
}

.brand-app-logo .voice-wave-right {
    right: 3px;
}

/* ---------- Custom home page links ---------- */
.custom-page-link {
    display: inline-flex;
    align-items: center;
    gap: 14px;
    text-decoration: none !important;
    color: var(--bv-ink) !important;
    font-weight: 800;
    font-size: 1rem;
    margin-top: 8px;
}

.custom-page-link .link-label {
    color: var(--bv-ink) !important;
}

.custom-page-link:visited,
.custom-page-link:active,
.custom-page-link:hover {
    color: var(--bv-ink) !important;
    opacity: 0.9;
}

.custom-page-link:visited .link-label,
.custom-page-link:active .link-label,
.custom-page-link:hover .link-label {
    color: var(--bv-ink) !important;
}

/* ---------- Mobile position fix ---------- */
@media screen and (max-width: 600px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 3.5rem;
    }

    .bv-hero-title {
        font-size: 1.9rem;
    }

    .bv-hero-sub {
        font-size: 0.92rem;
        margin-bottom: 24px;
    }

    .bv-tool-card {
        padding: 22px 22px 24px 22px;
        margin-bottom: 28px;
        align-items: flex-start;
    }

    .card-logo {
        margin-bottom: 10px;
    }

    .bv-tool-title {
        font-size: 1.45rem;
        line-height: 1.25;
        margin-bottom: 4px;
    }

    .bv-tool-desc {
        font-size: 1rem;
        line-height: 1.55;
        margin-bottom: 12px;
    }

    .custom-page-link {
        margin-top: 8px;
        gap: 14px;
        font-size: 1rem;
    }

    .app-logo {
        width: 48px;
        height: 48px;
        border-radius: 15px;
    }
}
</style>
"""

MAIN_LOGO_HTML = '<span class="app-logo voice-logo brand-app-logo"><span class="voice-bar voice-bar-one"></span><span class="voice-bar voice-bar-two"></span><span class="voice-bar voice-bar-three"></span><span class="voice-wave voice-wave-left"></span><span class="voice-wave voice-wave-right"></span></span>'

TRANSLATION_LOGO_HTML = '<span class="app-logo translation-logo"><span class="logo-bubble logo-a">A</span><span class="logo-bubble logo-b">文</span><span class="logo-bubble logo-c">ع</span><span class="logo-arrow arrow-one"></span><span class="logo-arrow arrow-two"></span></span>'

TTS_LOGO_HTML = '<span class="app-logo voice-logo"><span class="voice-bar voice-bar-one"></span><span class="voice-bar voice-bar-two"></span><span class="voice-bar voice-bar-three"></span><span class="voice-wave voice-wave-left"></span><span class="voice-wave voice-wave-right"></span></span>'

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(page_title="Bakhteyar-AI", page_icon="🟣", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# CUSTOM SIDEBAR
# ----------------------------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 10px 20px 10px;">
            <div class="bv-side-title">Bakhteyar-AI</div>
            <div class="bv-side-sub">Balochi Language Tools</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link("app.py", label="Home", icon="🏠")
    st.page_link("pages/1_🌐_Translation.py", label="Translation", icon="🌐")
    st.page_link("pages/2_🔊_Text_to_Speech.py", label="Text to Speech", icon="🔊")

# ----------------------------------------------------------------------------
# MAIN PAGE
# ----------------------------------------------------------------------------

with st.container(key="topbar"):
    st.markdown(
        f"""
        <div class="bv-brand">
            {MAIN_LOGO_HTML}
            <span class="bv-brand-name">Bakhteyar<span class="accent">-AI</span></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    '<div class="bv-hero-title">Balochi Language AI Tools</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="bv-hero-sub">
        Welcome to Bakhteyar-AI &mdash; a set of tools built for the Balochi language.
        Translate English text into Balochi, or turn Balochi text into natural-sounding
        speech, in both Latin and Arabic script.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# TOOL CARDS
# ----------------------------------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f'<div class="bv-tool-card"><div class="card-logo">{TRANSLATION_LOGO_HTML}</div><div class="bv-tool-title">Text to Text Translation</div><div class="bv-tool-desc">Translate English text into Balochi. Choose Latin or Arabic script for the output.</div><a class="custom-page-link" href="./Translation" target="_self">{TRANSLATION_LOGO_HTML}<span class="link-label">Open Translation</span></a></div>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f'<div class="bv-tool-card"><div class="card-logo">{TTS_LOGO_HTML}</div><div class="bv-tool-title">Text to Speech</div><div class="bv-tool-desc">Type Balochi text in Latin or Arabic script and generate natural-sounding speech.</div><a class="custom-page-link" href="./Text_to_Speech" target="_self">{TTS_LOGO_HTML}<span class="link-label">Open Text to Speech</span></a></div>',
        unsafe_allow_html=True,
    )
