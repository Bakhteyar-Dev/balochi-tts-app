import io
import wave

import numpy as np
import streamlit as st
import torch
from transformers import AutoTokenizer, VitsModel

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------

MODELS = {
    "latin": {
        "id": "facebook/mms-tts-bcc-script_latin",
        "label": "Latin",
        "placeholder": "Type Latin-script Balochi text here... (e.g. Tau choon haal e?)",
        "direction": "ltr",
        "align": "left",
        "font": "'Inter', sans-serif",
    },
    "arabic": {
        "id": "facebook/mms-tts-bcc-script_arabic",
        "label": "Arabic",
        "placeholder": "بلوچی متن عربی رسم الخط ءَ ا گدا بنویس...",
        "direction": "rtl",
        "align": "right",
        "font": "'Noto Naskh Arabic', serif",
    },
}

STAR_LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"]

# ----------------------------------------------------------------------------
# STYLES
# ----------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap');

:root {
    --bv-ink: #14181b;
    --bv-muted: #5f6b73;
    --bv-border: #e6e9eb;
    --bv-bg-soft: #f7f8f9;
    --bv-purple: #6f3fdc;
    --bv-purple-dark: #5a2fc2;
    --bv-card-radius: 16px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--bv-ink); }
.block-container { padding-top: 1.2rem; max-width: 820px; }

/* ---------- Top bar / logo ---------- */
.bv-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 8px 4px 22px 4px;
    border-bottom: 1px solid var(--bv-border);
    margin-bottom: 30px;
}
.bv-brand { display: flex; align-items: center; gap: 12px; }
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
    font-weight: 800;
    letter-spacing: -0.02em;
}
.bv-brand-name .accent { color: var(--bv-purple); }
.bv-brand-tag {
    font-size: 0.7rem;
    font-weight: 600;
    color: var(--bv-muted);
    background: var(--bv-bg-soft);
    border: 1px solid var(--bv-border);
    padding: 2px 9px;
    border-radius: 999px;
}

/* ---------- Hero ---------- */
.bv-hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 8px;
    line-height: 1.15;
}
.bv-hero-sub {
    font-size: 1rem;
    color: var(--bv-muted);
    max-width: 620px;
    line-height: 1.55;
    margin-bottom: 28px;
}

/* ---------- Section card ---------- */
.bv-card {
    background: white;
    border: 1px solid var(--bv-border);
    border-radius: var(--bv-card-radius);
    padding: 24px 26px;
    margin-bottom: 20px;
}
.bv-section-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 4px; }
.bv-section-caption { font-size: 0.85rem; color: var(--bv-muted); margin-bottom: 18px; }

/* ---------- Segmented script switch ---------- */
.bv-switch-wrap { display: flex; justify-content: center; margin-bottom: 22px; }
div[data-testid="stHorizontalBlock"]:has(button[kind]) {
    background: var(--bv-bg-soft);
    border: 1px solid var(--bv-border);
    border-radius: 999px;
    padding: 4px;
    width: fit-content;
    margin: 0 auto 22px auto;
    gap: 4px !important;
}
div[data-testid="stHorizontalBlock"]:has(button[kind]) > div {
    width: auto !important;
    flex: none !important;
}
div[data-testid="stHorizontalBlock"]:has(button[kind]) button {
    border-radius: 999px !important;
    padding: 0.45rem 1.6rem !important;
    font-weight: 700 !important;
    border: none !important;
    transition: all 0.15s ease;
}
div[data-testid="stHorizontalBlock"]:has(button[kind]) button[kind="primary"] {
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark)) !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(111, 63, 220, 0.3);
}
div[data-testid="stHorizontalBlock"]:has(button[kind]) button[kind="secondary"] {
    background: transparent !important;
    color: var(--bv-muted) !important;
    box-shadow: none !important;
}
div[data-testid="stHorizontalBlock"]:has(button[kind]) button[kind="secondary"]:hover {
    color: var(--bv-ink) !important;
}

/* ---------- Primary action button ---------- */
div[data-testid="stButton"] button[data-testid="baseButton-primary"],
.bv-generate-btn button[kind="primary"] {
    background: linear-gradient(135deg, var(--bv-purple), var(--bv-purple-dark));
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.4rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(111, 63, 220, 0.28);
}

/* ---------- Misc ---------- */
.bv-avg-rating { font-size: 0.85rem; color: var(--bv-muted); margin-top: 6px; }
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
# MODEL LOADING / INFERENCE
# ----------------------------------------------------------------------------


@st.cache_resource(show_spinner=False)
def load_tts_model(model_id: str):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = VitsModel.from_pretrained(model_id).to(device)
    model.eval()
    return tokenizer, model, device


def waveform_to_wav_bytes(waveform, sampling_rate):
    waveform = np.clip(waveform, -1.0, 1.0)
    audio_int16 = (waveform * 32767).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sampling_rate)
        wav_file.writeframes(audio_int16.tobytes())

    return buffer.getvalue()


def text_to_speech(text: str, script_key: str):
    model_id = MODELS[script_key]["id"]
    tokenizer, model, device = load_tts_model(model_id)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        waveform = model(**inputs).waveform

    waveform = waveform.squeeze().detach().cpu().numpy()
    return waveform_to_wav_bytes(waveform, model.config.sampling_rate)


# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------

if "script_key" not in st.session_state:
    st.session_state.script_key = "latin"
if "result" not in st.session_state:
    st.session_state.result = None
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(page_title="BakhtAI Voice", page_icon="🎙️", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---- Top bar / logo ----
st.markdown(
    f"""
    <div class="bv-topbar">
        <div class="bv-brand">
            <div class="bv-logo-mark">{LOGO_SVG}</div>
            <span class="bv-brand-name">Bakht<span class="accent">AI</span> Voice</span>
        </div>
        <span class="bv-brand-tag">Beta</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Hero ----
st.markdown('<div class="bv-hero-title">Balochi Text to Speech</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="bv-hero-sub">
        Type Balochi text in Latin or Arabic script and generate natural-sounding speech
        in seconds.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# INPUT CARD
# ----------------------------------------------------------------------------

st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<div class="bv-section-title">Enter your text</div>', unsafe_allow_html=True)
st.markdown('<div class="bv-section-caption">Switch the script, then type your Balochi text below.</div>', unsafe_allow_html=True)

# ---- Segmented script switch ----
sw_col1, sw_col2 = st.columns(2)
with sw_col1:
    if st.button(
        "Latin",
        type="primary" if st.session_state.script_key == "latin" else "secondary",
        use_container_width=True,
        key="btn_latin",
    ):
        st.session_state.script_key = "latin"
        st.rerun()
with sw_col2:
    if st.button(
        "Arabic",
        type="primary" if st.session_state.script_key == "arabic" else "secondary",
        use_container_width=True,
        key="btn_arabic",
    ):
        st.session_state.script_key = "arabic"
        st.rerun()

script_choice = st.session_state.script_key
current = MODELS[script_choice]

# Apply text direction / font dynamically based on the selected script
st.markdown(
    f"""
    <style>
    div[data-testid="stTextArea"] textarea {{
        direction: {current['direction']};
        text-align: {current['align']};
        font-family: {current['font']};
        font-size: 1.05rem;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

text = st.text_area(
    "Enter Balochi text",
    height=160,
    placeholder=current["placeholder"],
    label_visibility="collapsed",
    key="bv_text_input",
)

generate_clicked = st.button("Generate Speech", type="primary", use_container_width=True, key="btn_generate")
st.markdown("</div>", unsafe_allow_html=True)

# ----------------------------------------------------------------------------
# GENERATION
# ----------------------------------------------------------------------------

if generate_clicked:
    clean_text = text.strip()
    if not clean_text:
        st.warning("Please enter Balochi text first.")
    else:
        with st.spinner(f"Generating speech ({current['label']} script)..."):
            try:
                wav_bytes = text_to_speech(clean_text, script_choice)
                st.session_state.result = {
                    "wav": wav_bytes,
                    "text": clean_text,
                    "script": script_choice,
                    "rated": False,
                }
            except Exception as error:
                st.session_state.result = None
                st.error(f"Could not generate speech: {error}")

# ----------------------------------------------------------------------------
# RESULT + FEEDBACK
# ----------------------------------------------------------------------------

if st.session_state.result:
    result = st.session_state.result

    st.markdown('<div class="bv-card">', unsafe_allow_html=True)
    st.markdown('<div class="bv-section-title">Result</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="bv-section-caption">{MODELS[result["script"]]["label"]} script</div>', unsafe_allow_html=True)

    st.audio(result["wav"], format="audio/wav")

    st.download_button(
        "Download WAV",
        data=result["wav"],
        file_name=f"bakhtai_voice_{result['script']}.wav",
        mime="audio/wav",
        use_container_width=True,
    )

    st.markdown('<div class="bv-section-title" style="font-size:0.95rem; margin-top:20px;">Rate this audio</div>', unsafe_allow_html=True)

    has_native_feedback = hasattr(st, "feedback")

    if has_native_feedback:
        rating = st.feedback("stars", key=f"rating_{id(result)}")
        if rating is not None and not result["rated"]:
            st.session_state.feedback_log.append(rating + 1)
            st.session_state.result["rated"] = True
            st.toast(f"Thanks for rating it {STAR_LABELS[rating]}!", icon="⭐")
    else:
        rating_label = st.radio(
            "Rate this audio",
            options=STAR_LABELS,
            horizontal=True,
            label_visibility="collapsed",
            key=f"rating_fallback_{id(result)}",
            index=None,
        )
        if rating_label and not result["rated"]:
            st.session_state.feedback_log.append(STAR_LABELS.index(rating_label) + 1)
            st.session_state.result["rated"] = True
            st.toast(f"Thanks for rating it {rating_label}!", icon="⭐")

    if st.session_state.feedback_log:
        avg = sum(st.session_state.feedback_log) / len(st.session_state.feedback_log)
        st.markdown(
            f'<div class="bv-avg-rating">Average rating: {avg:.1f} / 5 '
            f'from {len(st.session_state.feedback_log)} rating(s)</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
