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

.bv-tool-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 14px;
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

/* ---------- Main page open buttons only ---------- */
div[data-testid="stMain"] div[data-testid="stPageLink"] a {
    background: linear-gradient(135deg, #8a5cf0, #6f3fdc) !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: 800 !important;
    justify-content: center !important;
    padding: 0.65rem 1rem !important;
    box-shadow: 0 6px 16px rgba(111, 63, 220, 0.24) !important;
}

div[data-testid="stMain"] div[data-testid="stPageLink"] a p,
div[data-testid="stMain"] div[data-testid="stPageLink"] a span {
    color: white !important;
}

div[data-testid="stMain"] div[data-testid="stPageLink"] a:hover {
    opacity: 0.92 !important;
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
        """
        <div class="bv-tool-card">
            <div class="bv-tool-icon">🌐</div>
            <div class="bv-tool-title">Text to Text Translation</div>
            <div class="bv-tool-desc">
                Translate English text into Balochi. Choose Latin or Arabic script
                for the output.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link(
        "pages/1_🌐_Translation.py",
        label="Open Translation",
        icon="🌐"
    )

with col2:
    st.markdown(
        """
        <div class="bv-tool-card">
            <div class="bv-tool-icon">🔊</div>
            <div class="bv-tool-title">Text to Speech</div>
            <div class="bv-tool-desc">
                Type Balochi text in Latin or Arabic script and generate
                natural-sounding speech.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.page_link(
        "pages/2_🔊_Text_to_Speech.py",
        label="Open Text to Speech",
        icon="🔊"
    )
