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

.bv-logo-mark {
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
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
    margin-bottom: 18px;
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

.card-logo {
    margin-bottom: 18px;
}

/* Translation logo */
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

/* Text to speech logo */
.tts-logo {
    background: radial-gradient(circle at 50% 40%, #a855f7 0%, #6d28d9 45%, #3b0764 100%);
}

.tts-logo::before {
    content: "";
    position: absolute;
    width: 39px;
    height: 39px;
    border: 2px solid rgba(216, 180, 254, 0.75);
    border-radius: 50%;
    left: 6px;
    top: 6px;
    box-shadow: 0 0 14px rgba(216, 180, 254, 0.7);
}

.mic-head {
    position: absolute;
    width: 15px;
    height: 25px;
    border-radius: 10px;
    background: linear-gradient(180deg, #ffffff, #d8b4fe);
    left: 19px;
    top: 10px;
    z-index: 3;
}

.mic-stand {
    position: absolute;
    width: 20px;
    height: 16px;
    border: 3px solid #ffffff;
    border-top: none;
    border-radius: 0 0 12px 12px;
    left: 15px;
    top: 26px;
    z-index: 2;
}

.mic-stand::after {
    content: "";
    position: absolute;
    width: 3px;
    height: 8px;
    background: #ffffff;
    left: 8px;
    top: 13px;
    border-radius: 99px;
}

.wave {
    position: absolute;
    width: 10px;
    height: 24px;
    top: 15px;
    border-radius: 50%;
    border: 3px solid #e9d5ff;
    opacity: 0.9;
}

.wave-left {
    left: 5px;
    border-right: none;
}

.wave-right {
    right: 5px;
    border-left: none;
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
    margin-top: 20px;
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
        padding: 20px 18px;
        margin-bottom: 16px;
    }

    .app-logo {
        width: 48px;
        height: 48px;
        border-radius: 15px;
    }
}
</style>
"""

LOGO_SVG = """
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="9" width="3" height="6" rx="1.5" fill="white" opacity="0.55"/>
    <rect x="8" y="5" width="3" height="14" rx="1.5" fill="white"/>
    <rect x="13" y="2" width="3" height="20" rx="1.5" fill="white" opacity="0.85"/>
    <rect x="18" y="7" width="3" height="10" rx="1.5" fill="white" opacity="0.55"/>
</svg>
"""

TRANSLATION_LOGO_HTML = '<span class="app-logo translation-logo"><span class="logo-bubble logo-a">A</span><span class="logo-bubble logo-b">文</span><span class="logo-bubble logo-c">ع</span><span class="logo-arrow arrow-one"></span><span class="logo-arrow arrow-two"></span></span>'

TTS_LOGO_HTML = '<span class="app-logo tts-logo"><span class="mic-head"></span><span class="mic-stand"></span><span class="wave wave-left"></span><span class="wave wave-right"></span></span>'

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
            <div class="bv-logo-mark">{LOGO_SVG}</div>
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
        f"""
        <div class="bv-tool-card">
            <div class="card-logo">{TRANSLATION_LOGO_HTML}</div>
            <div class="bv-tool-title">Text to Text Translation</div>
            <div class="bv-tool-desc">
                Translate English text into Balochi. Choose Latin or Arabic script
                for the output.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<a class="custom-page-link" href="./Translation" target="_self">{TRANSLATION_LOGO_HTML}<span class="link-label">Open Translation</span></a>',
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="bv-tool-card">
            <div class="card-logo">{TTS_LOGO_HTML}</div>
            <div class="bv-tool-title">Text to Speech</div>
            <div class="bv-tool-desc">
                Type Balochi text in Latin or Arabic script and generate
                natural-sounding speech.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<a class="custom-page-link" href="./Text_to_Speech" target="_self">{TTS_LOGO_HTML}<span class="link-label">Open Text to Speech</span></a>',
        unsafe_allow_html=True,
    )
