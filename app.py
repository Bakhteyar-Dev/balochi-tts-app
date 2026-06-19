import io
import csv
import wave
from datetime import datetime
from pathlib import Path

import numpy as np
import streamlit as st
import torch
from transformers import AutoTokenizer, VitsModel


TTS_MODEL_IDS = {
    "Latin Script": "facebook/mms-tts-bcc-script_latin",
    "Arabic Script": "facebook/mms-tts-bcc-script_arabic",
}
FEEDBACK_FILE = Path("feedback.csv")


@st.cache_resource
def load_tts_model(script_name):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model_id = TTS_MODEL_IDS[script_name]
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


def text_to_speech(text, script_name):
    tokenizer, model, device = load_tts_model(script_name)

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


def save_feedback(script_name, rating, feedback, source_text):
    file_exists = FEEDBACK_FILE.exists()
    with FEEDBACK_FILE.open("a", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=["time", "script", "rating", "feedback", "text"],
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "script": script_name,
                "rating": rating,
                "feedback": feedback,
                "text": source_text,
            }
        )


st.set_page_config(
    page_title="Neurolingo",
    page_icon="audio",
    layout="wide",
)

if "wav_bytes" not in st.session_state:
    st.session_state.wav_bytes = None
if "last_script_name" not in st.session_state:
    st.session_state.last_script_name = "Latin Script"
if "last_text" not in st.session_state:
    st.session_state.last_text = ""
if "rating_submitted" not in st.session_state:
    st.session_state.rating_submitted = False

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');

    :root {
        --ink: #0a1628;
        --muted: #506176;
        --soft: #f4fbff;
        --panel: rgba(255, 255, 255, 0.86);
        --line: rgba(14, 116, 144, 0.18);
        --blue: #0b5cad;
        --sky: #12a8ef;
        --mint: #0f766e;
        --amber: #d98b1f;
        --shadow: 0 24px 70px rgba(15, 23, 42, 0.11);
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        background:
            linear-gradient(115deg, rgba(255,255,255,0.92), rgba(235,247,255,0.88)),
            radial-gradient(circle at 14% 12%, rgba(18,168,239,0.20), transparent 32%),
            radial-gradient(circle at 86% 80%, rgba(217,139,31,0.15), transparent 28%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.4rem;
        padding-bottom: 2.2rem;
    }

    .app-shell {
        border: 1px solid rgba(191, 221, 251, 0.75);
        border-radius: 34px;
        padding: 28px;
        background: rgba(255, 255, 255, 0.54);
        box-shadow: var(--shadow);
        backdrop-filter: blur(18px);
    }

    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 24px;
        margin-bottom: 26px;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 18px;
    }

    .logo {
        width: 76px;
        height: 58px;
        border-radius: 20px;
        display: grid;
        place-items: center;
        color: #ffffff;
        font-size: 30px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--sky), #5145e8);
        box-shadow: 0 16px 30px rgba(37, 99, 235, 0.24);
    }

    .brand-title {
        margin: 0;
        color: #000000;
        font-size: clamp(34px, 5vw, 52px);
        line-height: 0.95;
        font-weight: 800;
        letter-spacing: 0;
    }

    .brand-subtitle {
        margin-top: 8px;
        color: #182235;
        font-size: 16px;
        font-weight: 600;
    }

    .status-pill {
        border-radius: 999px;
        padding: 12px 20px;
        background: #0b5cad;
        color: #ffffff;
        font-size: 14px;
        font-weight: 800;
        box-shadow: 0 16px 34px rgba(11, 92, 173, 0.22);
        white-space: nowrap;
    }

    .studio {
        border: 1px solid var(--line);
        border-radius: 28px;
        padding: 24px;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.92), rgba(243,250,255,0.82));
    }

    .panel {
        min-height: 360px;
        border: 1px solid rgba(191, 221, 251, 0.9);
        border-radius: 24px;
        padding: 18px;
        background: rgba(255, 255, 255, 0.88);
        box-shadow: 0 14px 36px rgba(15, 23, 42, 0.06);
    }

    .panel-title {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        border: 1px solid #9ed4ff;
        border-radius: 999px;
        padding: 9px 17px;
        margin-bottom: 14px;
        background: linear-gradient(135deg, #ffffff, #e9f7ff);
        color: #000000;
        font-size: 15px;
        font-weight: 800;
    }

    .script-line {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 14px;
        color: var(--muted);
        font-size: 13px;
        font-weight: 800;
    }

    .script-badge {
        border-radius: 999px;
        padding: 8px 12px;
        background: #eef8ff;
        color: #0b5cad;
        border: 1px solid #bfddfb;
    }

    div[data-testid="stTextArea"] label {
        font-size: 0;
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 238px;
        border-radius: 20px;
        border: 1px solid rgba(191, 221, 251, 0.95);
        background: #ffffff;
        color: var(--ink);
        font-size: 17px;
        line-height: 1.65;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.9);
    }

    div[data-testid="stTextArea"] textarea:focus {
        border-color: #0b5cad;
        box-shadow: 0 0 0 3px rgba(11, 92, 173, 0.12);
    }

    .stButton > button {
        width: 100%;
        border: none;
        border-radius: 22px;
        padding: 0.92rem 1.1rem;
        color: #ffffff;
        background: linear-gradient(135deg, #0b5cad, #084b91);
        font-size: 18px;
        font-weight: 800;
        box-shadow: 0 16px 34px rgba(11, 92, 173, 0.28);
    }

    .stButton > button:hover {
        border: none;
        color: #ffffff;
        background: linear-gradient(135deg, #116dc5, #08437f);
    }

    .audio-stage {
        min-height: 238px;
        border-radius: 20px;
        border: 1px solid rgba(191, 221, 251, 0.95);
        background:
            linear-gradient(135deg, rgba(255,255,255,0.96), rgba(242,249,255,0.92));
        padding: 20px;
        display: grid;
        align-content: center;
    }

    .empty-audio {
        min-height: 190px;
        display: grid;
        place-items: center;
        color: #8a98aa;
        font-size: 46px;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid #9ed4ff;
        color: #0b5cad;
        background: #ffffff;
        font-weight: 800;
    }

    .rating-card {
        margin-top: 22px;
        border: 1px solid rgba(191, 221, 251, 0.9);
        border-radius: 22px;
        padding: 18px;
        background: rgba(255,255,255,0.72);
    }

    .rating-title {
        margin: 0 0 10px 0;
        color: #000000;
        font-size: 16px;
        font-weight: 800;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-weight: 800;
        color: var(--ink);
    }

    div[data-testid="stToggle"] {
        margin-top: -4.25rem;
        margin-left: auto;
        width: fit-content;
    }

    div[data-testid="stToggle"] label {
        border: 1px solid #d7e7f7;
        border-radius: 999px;
        padding: 9px 14px;
        background: #ffffff;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
        font-weight: 800;
        color: var(--ink);
    }

    @media (max-width: 780px) {
        .block-container {
            padding: 1rem;
        }

        .app-shell {
            border-radius: 24px;
            padding: 16px;
        }

        .topbar,
        .brand {
            align-items: flex-start;
            flex-direction: column;
        }

        .status-pill {
            white-space: normal;
        }

        .studio,
        .panel {
            border-radius: 20px;
            padding: 16px;
        }

        div[data-testid="stToggle"] {
            margin: 0 0 14px 0;
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-shell">
        <div class="topbar">
            <div class="brand">
                <div class="logo">NL</div>
                <div>
                    <h1 class="brand-title">Neurolingo</h1>
                    <div class="brand-subtitle">Balochi Text-to-Speech Studio</div>
                </div>
            </div>
            <div class="status-pill">Voice Generator</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

use_arabic_script = st.toggle("Arabic script", value=False)

script_name = "Arabic Script" if use_arabic_script else "Latin Script"
script_hint = "Arabic-script Balochi text" if use_arabic_script else "Latin-script Balochi text"
script_label = "Arabic" if use_arabic_script else "Latin"

st.markdown('<div class="studio">', unsafe_allow_html=True)

input_col, output_col = st.columns(2, gap="large")

with input_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Input Text</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="script-line">
            <span>Write Balochi text</span>
            <span class="script-badge">{script_label} script</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    text = st.text_area(
        "Text input",
        height=238,
        placeholder=f"Type {script_hint} here...",
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

with output_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Generated Speech</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="script-line">
            <span>Audio result</span>
            <span class="script-badge">{script_label} voice</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="audio-stage">', unsafe_allow_html=True)
    if st.session_state.wav_bytes:
        st.audio(st.session_state.wav_bytes, format="audio/wav")
        st.download_button(
            "Download Speech",
            data=st.session_state.wav_bytes,
            file_name=f"neurolingo_{st.session_state.last_script_name.lower().replace(' ', '_')}.wav",
            mime="audio/wav",
        )
    else:
        st.markdown('<div class="empty-audio">&#9835;</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

left_space, action_col, right_space = st.columns([1, 2, 1])
with action_col:
    generate_clicked = st.button("Generate Speech", type="primary")

if generate_clicked:
    clean_text = text.strip()

    if not clean_text:
        st.warning("Please enter Balochi text first.")
    else:
        with st.spinner("Generating speech..."):
            try:
                wav_bytes = text_to_speech(clean_text, script_name)
                st.session_state.wav_bytes = wav_bytes
                st.session_state.last_script_name = script_name
                st.session_state.last_text = clean_text
                st.session_state.rating_submitted = False
                st.rerun()
            except Exception as error:
                st.error(f"Could not generate speech: {error}")

if st.session_state.wav_bytes:
    st.markdown('<div class="rating-card">', unsafe_allow_html=True)
    st.markdown('<p class="rating-title">Rate Speech Quality</p>', unsafe_allow_html=True)
    with st.form("speech_quality_feedback", clear_on_submit=True):
        rating = st.selectbox(
            "Quality rating",
            ["5 - Excellent", "4 - Good", "3 - Average", "2 - Poor", "1 - Very poor"],
        )
        feedback = st.text_input("Feedback", placeholder="Optional feedback")
        submitted = st.form_submit_button("Submit Rating")

    if submitted:
        save_feedback(
            st.session_state.last_script_name,
            rating,
            feedback,
            st.session_state.last_text,
        )
        st.session_state.rating_submitted = True
        st.session_state.last_feedback = {
            "time": datetime.now().isoformat(timespec="seconds"),
            "script": st.session_state.last_script_name,
            "rating": rating,
            "feedback": feedback,
        }

    if st.session_state.rating_submitted:
        st.success("Thank you. Your speech quality rating was submitted successfully.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
