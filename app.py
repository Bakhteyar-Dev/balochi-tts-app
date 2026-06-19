import io
import wave
from datetime import datetime

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
        "native_label": "Latin Script",
        "direction": "ltr",
        "align": "left",
        "placeholder": "Type Latin-script Balochi text here... (e.g. Tau choon haal e?)",
        "font": "'Inter', sans-serif",
    },
    "arabic": {
        "id": "facebook/mms-tts-bcc-script_arabic",
        "label": "Arabic",
        "native_label": "عربی رسم الخط",
        "direction": "rtl",
        "align": "right",
        "placeholder": "بلوچی متن عربی رسم الخط ءَ ا گدا بنویس...",
        "font": "'Noto Naskh Arabic', serif",
    },
}

STAR_LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"]

# ----------------------------------------------------------------------------
# STYLES
# ----------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap');

:root {
    --bv-primary: #0f6e6c;
    --bv-primary-dark: #0a4f4d;
    --bv-accent: #d99a2b;
    --bv-bg-card: #ffffff;
    --bv-bg-soft: #f4f8f7;
    --bv-text: #1c2b2a;
    --bv-muted: #6b7d7c;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 1.5rem;
    max-width: 760px;
}

/* ---------- Header ---------- */
.bv-header {
    background: linear-gradient(135deg, var(--bv-primary) 0%, var(--bv-primary-dark) 100%);
    border-radius: 18px;
    padding: 28px 32px;
    margin-bottom: 24px;
    box-shadow: 0 8px 24px rgba(15, 110, 108, 0.25);
    color: white;
    position: relative;
    overflow: hidden;
}
.bv-header::after {
    content: "";
    position: absolute;
    top: -40px;
    right: -40px;
    width: 160px;
    height: 160px;
    background: rgba(217, 154, 43, 0.25);
    border-radius: 50%;
}
.bv-header-title {
    font-size: 2.1rem;
    font-weight: 700;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 10px;
    letter-spacing: -0.02em;
}
.bv-header-badge {
    background: var(--bv-accent);
    color: #1c2b2a;
    font-size: 0.62rem;
    font-weight: 700;
    padding: 3px 9px;
    border-radius: 999px;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    vertical-align: middle;
}
.bv-header-sub {
    margin-top: 6px;
    font-size: 0.95rem;
    color: rgba(255,255,255,0.85);
    font-weight: 400;
}

/* ---------- Card ---------- */
.bv-card {
    background: var(--bv-bg-card);
    border-radius: 16px;
    padding: 20px 22px;
    border: 1px solid #e4ece9;
    margin-bottom: 18px;
}
.bv-section-label {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--bv-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}

/* ---------- Script toggle (radio as pills) ---------- */
div[data-testid="stRadio"] > div {
    flex-direction: row;
    gap: 10px;
    background: var(--bv-bg-soft);
    padding: 5px;
    border-radius: 999px;
    width: fit-content;
}
div[data-testid="stRadio"] label {
    background: transparent;
    border-radius: 999px;
    padding: 6px 18px;
    margin: 0;
    transition: all 0.15s ease;
    cursor: pointer;
}
div[data-testid="stRadio"] label:has(input:checked) {
    background: var(--bv-primary);
}
div[data-testid="stRadio"] label:has(input:checked) p {
    color: white !important;
    font-weight: 600;
}
div[data-testid="stRadio"] input {
    display: none;
}

/* ---------- Generate button ---------- */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, var(--bv-primary) 0%, var(--bv-primary-dark) 100%);
    border: none;
    border-radius: 12px;
    padding: 0.6rem 1.4rem;
    font-weight: 600;
    box-shadow: 0 4px 12px rgba(15, 110, 108, 0.3);
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(15, 110, 108, 0.4);
}

/* ---------- Misc ---------- */
.bv-footer-note {
    text-align: center;
    color: var(--bv-muted);
    font-size: 0.78rem;
    margin-top: 28px;
}
.bv-avg-rating {
    font-size: 0.85rem;
    color: var(--bv-muted);
}
</style>
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

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=256,
    )
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
    st.session_state.result = None  # {"wav": bytes, "text": str, "script": str}
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []  # list of ints 1-5

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(
    page_title="BakhtAI Voice",
    page_icon="🎙️",
    layout="centered",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.markdown(
    """
    <div class="bv-header">
        <p class="bv-header-title">🎙️ BakhtAI Voice <span class="bv-header-badge">Beta</span></p>
        <p class="bv-header-sub">Balochi text-to-speech &middot; Latin &amp; Arabic script</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# SCRIPT TOGGLE
# ----------------------------------------------------------------------------

st.markdown('<div class="bv-card">', unsafe_allow_html=True)
st.markdown('<div class="bv-section-label">Script</div>', unsafe_allow_html=True)

script_choice = st.radio(
    "Script",
    options=list(MODELS.keys()),
    format_func=lambda k: MODELS[k]["native_label"],
    horizontal=True,
    label_visibility="collapsed",
    key="script_key",
)

current = MODELS[script_choice]

# Apply text direction dynamically based on the selected script
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

generate_clicked = st.button("Generate Speech", type="primary", use_container_width=True)
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
    st.markdown('<div class="bv-section-label">Result</div>', unsafe_allow_html=True)

    st.audio(result["wav"], format="audio/wav")

    st.download_button(
        "Download WAV",
        data=result["wav"],
        file_name=f"bakhtai_voice_{result['script']}.wav",
        mime="audio/wav",
        use_container_width=True,
    )

    st.markdown('<div class="bv-section-label" style="margin-top:18px;">Rate this audio</div>', unsafe_allow_html=True)

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

st.markdown(
    '<div class="bv-footer-note">BakhtAI Voice runs on Meta MMS-TTS models for Balochi (bcc).</div>',
    unsafe_allow_html=True,
)
