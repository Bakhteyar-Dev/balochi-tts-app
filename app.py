import streamlit as st

from bv_ui import (
    ASR_ICON,
    DATA_ICON,
    OCR_ICON,
    TRANSLATION_ICON,
    TTS_ICON,
    inject_theme,
    render_footer,
    render_sidebar,
    render_topbar,
)

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(
    page_title="Bakhteyar-AI",
    page_icon="🟣",
    layout="centered",
    initial_sidebar_state="expanded",
)
inject_theme()
render_sidebar()
render_topbar()

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------

st.markdown('<span class="bv-eyebrow">Balochi Language AI</span>', unsafe_allow_html=True)

st.markdown(
    '<div class="bv-hero-title">AI tools for the <span class="grad">Balochi language</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="bv-hero-sub">
        Welcome to Bakhteyar-AI &mdash; a growing toolkit built for Balochi. Translate
        English into Balochi or turn Balochi text into natural-sounding speech, in both
        Latin and Arabic script.
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
        <div class="bv-card">
            <div class="bv-icon bv-icon-1">{TRANSLATION_ICON}</div>
            <div class="bv-card-title">Text Translation</div>
            <div class="bv-card-desc">
                Translate English text into Balochi. Choose Latin or Arabic script for the output.
            </div>
            <a class="bv-card-link" href="./Translation" target="_self">
                Open Translation <span class="arrow">&rarr;</span>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""
        <div class="bv-card">
            <div class="bv-icon bv-icon-2">{TTS_ICON}</div>
            <div class="bv-card-title">Text to Speech</div>
            <div class="bv-card-desc">
                Type Balochi text in Latin or Arabic script and generate natural-sounding speech.
            </div>
            <a class="bv-card-link" href="./Text_to_Speech" target="_self">
                Open Text to Speech <span class="arrow">&rarr;</span>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ----------------------------------------------------------------------------
# HOW TO USE
# ----------------------------------------------------------------------------

st.markdown('<div class="bv-kicker">Getting started</div>', unsafe_allow_html=True)
st.markdown('<div class="bv-h2">How to use the app</div>', unsafe_allow_html=True)

steps = [
    ("Pick a tool", "Open Translation or Text to Speech from the cards above or the sidebar."),
    ("Choose a script", "Switch between Balochi Latin and Arabic script with one tap."),
    ("Enter your text", "Type or paste your text into the input box."),
    ("Get the result", "Translate or generate speech, then copy or download the output."),
]

step_cols = st.columns(4)
for index, (title, desc) in enumerate(steps):
    with step_cols[index]:
        st.markdown(
            f"""
            <div class="bv-step">
                <div class="bv-step-num">{index + 1}</div>
                <div class="bv-step-title">{title}</div>
                <div class="bv-step-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# COMING SOON
# ----------------------------------------------------------------------------

st.markdown('<div class="bv-kicker">On the roadmap</div>', unsafe_allow_html=True)
st.markdown('<div class="bv-h2">Coming soon</div>', unsafe_allow_html=True)

coming = [
    (ASR_ICON, "Speech Recognition (ASR)", "Convert spoken Balochi to text in both Latin and Arabic script."),
    (OCR_ICON, "OCR", "Extract Balochi text from images and scanned documents."),
    (DATA_ICON, "Building Datasets", "Tools to collect and curate high-quality Balochi language datasets."),
]

soon_cols = st.columns(3)
for index, (icon, title, desc) in enumerate(coming):
    with soon_cols[index]:
        st.markdown(
            f"""
            <div class="bv-soon">
                <div class="bv-soon-badge">Soon</div>
                <div class="bv-soon-emoji">{icon}</div>
                <div class="bv-soon-title">{title}</div>
                <div class="bv-soon-desc">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ----------------------------------------------------------------------------
# FOOTER
# ----------------------------------------------------------------------------

render_footer()
