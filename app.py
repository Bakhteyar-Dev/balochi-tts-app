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
    --bv-orange: #f0901e;
    --bv-purple: #7c4ee0;
    --bv-blue: #1fb6dd;
    --bv-card-radius: 16px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--bv-ink); }
.block-container { padding-top: 1.2rem; max-width: 880px; }

/* ---------- Top bar ---------- */
.bv-topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 4px 22px 4px;
    border-bottom: 1px solid var(--bv-border);
    margin-bottom: 30px;
}
.bv-brand { display: flex; align-items: center; gap: 12px; }
.bv-brand-logo {
    font-size: 1.7rem;
    line-height: 1;
}
.bv-brand-name {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.bv-brand-tag {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--bv-muted);
    background: var(--bv-bg-soft);
    border: 1px solid var(--bv-border);
    padding: 2px 9px;
    border-radius: 999px;
}

/* ---------- Hero ---------- */
.bv-hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 10px;
    line-height: 1.1;
}
.bv-hero-sub {
    font-size: 1.05rem;
    color: var(--bv-muted);
    max-width: 640px;
    line-height: 1.55;
    margin-bottom: 28px;
}

/* ---------- Feature cards ---------- */
.bv-feature-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 36px;
}
.bv-feature-card {
    border-radius: var(--bv-card-radius);
    padding: 22px 20px;
    color: white;
    min-height: 130px;
}
.bv-feature-card.orange { background: linear-gradient(135deg, #f3a23d, #ea7e16); }
.bv-feature-card.purple { background: linear-gradient(135deg, #9a72ec, #6f3fdc); }
.bv-feature-card.blue   { background: linear-gradient(135deg, #3fc6e8, #149dc3); }
.bv-feature-icon { font-size: 1.4rem; margin-bottom: 10px; opacity: 0.95; }
.bv-feature-title { font-size: 1.05rem; font-weight: 700; margin-bottom: 6px; }
.bv-feature-desc { font-size: 0.84rem; line-height: 1.4; opacity: 0.92; }

/* ---------- Section card ---------- */
.bv-card {
    background: white;
    border: 1px solid var(--bv-border);
    border-radius: var(--bv-card-radius);
    padding: 24px 26px;
    margin-bottom: 20px;
}
.bv-section-title {
    font-size: 1.15rem;
    font-weight: 700;
    margin-bottom: 4px;
}
.bv-section-caption {
    font-size: 0.85rem;
    color: var(--bv-muted);
    margin-bottom: 18px;
}

/* ---------- Script switch row ---------- */
.bv-switch-row {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    background: var(--bv-bg-soft);
    border: 1px solid var(--bv-border);
    border-radius: 999px;
    padding: 10px 22px;
    width: fit-content;
    margin: 0 auto 24px auto;
}
.bv-switch-label {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--bv-muted);
    transition: color 0.15s ease;
}
.bv-switch-label.active.left { color: var(--bv-orange); }
.bv-switch-label.active.right { color: var(--bv-purple); }

div[data-testid="stToggle"] { display: flex; justify-content: center; }
div[data-testid="stToggle"] label { gap: 0; }

/* ---------- Buttons ---------- */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, var(--bv-purple), #5d2fc9);
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.4rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(124, 78, 224, 0.28);
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    transform: translateY(-1px);
    box-shadow: 0 8px 20px rgba(124, 78, 224, 0.38);
}

/* ---------- Misc ---------- */
.bv-avg-rating { font-size: 0.85rem; color: var(--bv-muted); margin-top: 6px; }
.bv-footer-note { text-align: center; color: var(--bv-muted); font-size: 0.78rem; margin-top: 30px; }

@media (max-width: 700px) {
    .bv-feature-grid { grid-template-columns: 1fr; }
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

    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=256)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        waveform = model(**inputs).waveform

    waveform = waveform.squeeze().detach().cpu().numpy()
    return waveform_to_wav_bytes(waveform, model.config.sampling_rate)


# ----------------------------------------------------------------------------
# SESSION STATE
# ----------------------------------------------------------------------------

if "use_arabic" not in st.session_state:
    st.session_state.use_arabic = False
if "result" not in st.session_state:
    st.session_state.result = None
if "feedback_log" not in st.session_state:
    st.session_state.feedback_log = []

# ----------------------------------------------------------------------------
# PAGE SETUP
# ----------------------------------------------------------------------------

st.set_page_config(page_title="BakhtAI Voice", page_icon="🎙️", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---- Top bar ----
st.markdown(
    """
    <div class="bv-topbar">
        <div class="bv-brand">
            <span class="bv-brand-logo">🎙️</span>
            <span class="bv-brand-name">BakhtAI Voice</span>
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
        BakhtAI Voice turns Balochi text into natural-sounding speech, in both Latin and
        Arabic script. Type your text, pick a script, and generate audio in seconds.
    </div>
    """,
    unsafe_allow_html=True,
)

# ---- Feature cards ----
st.markdown(
    """
    <div class="bv-feature-grid">
        <div class="bv-feature-card orange">
            <div class="bv-feature-icon">🅻</div>
            <div class="bv-feature-title">Latin Script</div>
            <div class="bv-feature-desc">Write Balochi using Latin letters, left-to-right.</div>
        </div>
        <div class="bv-feature-card purple">
            <div class="bv-feature-icon">🗨️</div>
            <div class="bv-feature-title">Arabic Script</div>
            <div class="bv-feature-desc">Write Balochi using Arabic letters, right-to-left.</div>
        </div>
        <div class="bv-feature-card blue">
            <div class="bv-feature-icon">🔊</div>
            <div class="bv-feature-title">Natural Voice</div>
            <div class="bv-feature-desc">Powered by Meta's MMS speech synthesis models.</div>
        </div>
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

# ---- Single toggle switch: Latin <-> Arabic ----
left_active = "active left" if not st.session_state.use_arabic else ""
right_active = "active right" if st.session_state.use_arabic else ""

st.markdown('<div class="bv-switch-row">', unsafe_allow_html=True)
sw_col1, sw_col2, sw_col3 = st.columns([1, 1, 1])
with sw_col1:
    st.markdown(f'<div class="bv-switch-label {left_active}" style="text-align:right;">Latin</div>', unsafe_allow_html=True)
with sw_col2:
    use_arabic = st.toggle("Switch script", key="use_arabic", label_visibility="collapsed")
with sw_col3:
    st.markdown(f'<div class="bv-switch-label {right_active}" style="text-align:left;">Arabic</div>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

script_choice = "arabic" if use_arabic else "latin"
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

st.markdown(
    '<div class="bv-footer-note">BakhtAI Voice runs on Meta MMS-TTS models for Balochi (bcc).</div>',
    unsafe_allow_html=True,
)
