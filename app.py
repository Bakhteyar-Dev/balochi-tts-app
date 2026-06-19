import csv
import io
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
    page_title="Balochi Text to Speech",
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
        --ink: #17202a;
        --muted: #5d6978;
        --paper: #fffaf1;
        --panel: rgba(255, 255, 255, 0.86);
        --line: rgba(35, 48, 66, 0.14);
        --teal: #0f766e;
        --teal-dark: #0b5d56;
        --gold: #c9811a;
        --rose: #a64253;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        background:
            linear-gradient(120deg, rgba(255,250,241,0.95), rgba(237,247,245,0.95)),
            repeating-linear-gradient(45deg, rgba(15,118,110,0.045) 0 1px, transparent 1px 18px);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1040px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .hero {
        border: 1px solid var(--line);
        border-radius: 28px;
        padding: 34px;
        background:
            linear-gradient(135deg, rgba(255,255,255,0.94), rgba(248,242,231,0.9)),
            radial-gradient(circle at 96% 12%, rgba(201,129,26,0.18), transparent 30%);
        box-shadow: 0 26px 70px rgba(23, 32, 42, 0.12);
        margin-bottom: 22px;
    }

    .brand-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 18px;
        margin-bottom: 26px;
    }

    .brand-mark {
        width: 56px;
        height: 56px;
        border-radius: 18px;
        display: grid;
        place-items: center;
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--teal), var(--gold));
        box-shadow: 0 14px 30px rgba(15, 118, 110, 0.24);
    }

    .script-pill {
        border: 1px solid rgba(15,118,110,0.22);
        border-radius: 999px;
        padding: 10px 14px;
        color: var(--teal-dark);
        background: rgba(255, 255, 255, 0.72);
        font-size: 13px;
        font-weight: 700;
    }

    .hero h1 {
        font-size: clamp(34px, 6vw, 62px);
        line-height: 1;
        letter-spacing: 0;
        margin: 0 0 14px 0;
        color: var(--ink);
    }

    .hero p {
        max-width: 680px;
        margin: 0;
        color: var(--muted);
        font-size: 18px;
        line-height: 1.6;
    }

    .workspace {
        border: 1px solid var(--line);
        border-radius: 24px;
        background: var(--panel);
        box-shadow: 0 18px 48px rgba(23, 32, 42, 0.08);
        padding: 24px;
    }

    .section-title {
        margin: 0 0 6px 0;
        font-size: 18px;
        font-weight: 800;
        color: var(--ink);
    }

    .section-copy {
        margin: 0 0 16px 0;
        color: var(--muted);
        font-size: 14px;
    }

    div[data-testid="stTextArea"] label,
    div[data-testid="stToggle"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-weight: 800;
        color: var(--ink);
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 190px;
        border-radius: 18px;
        border: 1px solid rgba(15,118,110,0.24);
        background: #fffdf8;
        color: var(--ink);
        font-size: 17px;
        line-height: 1.65;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.9);
    }

    .stButton > button {
        width: 100%;
        border-radius: 16px;
        border: 0;
        padding: 0.85rem 1rem;
        background: linear-gradient(135deg, var(--teal), var(--teal-dark));
        color: white;
        font-weight: 800;
        box-shadow: 0 16px 34px rgba(15, 118, 110, 0.25);
    }

    .stButton > button:hover {
        border: 0;
        color: white;
        background: linear-gradient(135deg, #12867d, #094c47);
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid rgba(166, 66, 83, 0.28);
        color: var(--rose);
        background: rgba(255,255,255,0.86);
        font-weight: 800;
    }

    .audio-box {
        border-radius: 20px;
        border: 1px solid rgba(201,129,26,0.28);
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,248,235,0.85));
        padding: 18px;
        margin-top: 18px;
    }

    .empty-audio {
        min-height: 120px;
        display: grid;
        place-items: center;
        color: #8a98aa;
        font-size: 38px;
    }

    .hint-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 10px;
        margin-top: 18px;
    }

    .hint {
        border-radius: 16px;
        border: 1px solid var(--line);
        padding: 13px;
        color: var(--muted);
        background: rgba(255,255,255,0.64);
        font-size: 13px;
        font-weight: 700;
    }

    .current-script {
        border: 1px solid rgba(15,118,110,0.22);
        border-radius: 16px;
        padding: 14px 16px;
        margin-bottom: 16px;
        color: var(--teal-dark);
        background: rgba(255,255,255,0.72);
        font-size: 14px;
        font-weight: 800;
    }

    .feedback-box {
        margin-top: 20px;
        border-top: 1px solid rgba(35, 48, 66, 0.14);
        padding-top: 16px;
    }

    @media (max-width: 720px) {
        .block-container {
            padding: 1rem;
        }

        .hero,
        .workspace {
            border-radius: 22px;
            padding: 20px;
        }

        .brand-row {
            align-items: flex-start;
            flex-direction: column;
            margin-bottom: 20px;
        }

        .script-pill {
            width: 100%;
            box-sizing: border-box;
            overflow-wrap: anywhere;
        }

        .hint-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="brand-row">
            <div class="brand-mark">BT</div>
            <div class="script-pill">Balochi voice generator</div>
        </div>
        <h1>Balochi Text to Speech</h1>
        <p>Type Balochi in your preferred script and generate clear spoken audio directly in the browser.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<main class="workspace">', unsafe_allow_html=True)
st.markdown('<p class="section-title">Create Speech</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="section-copy">Choose the script, enter text, then generate and download the audio as a WAV file.</p>',
    unsafe_allow_html=True,
)

use_arabic_script = st.toggle(
    "Turn on Balochi Arabic script voice",
    value=False,
)

script_name = "Arabic Script" if use_arabic_script else "Latin Script"
script_hint = "Latin-script Balochi text" if script_name == "Latin Script" else "Arabic-script Balochi text"

st.markdown(
    f'<div class="current-script">Current script: Balochi {script_name}</div>',
    unsafe_allow_html=True,
)

text = st.text_area(
    f"Enter {script_hint}",
    height=160,
    placeholder=f"Type {script_hint} here...",
)

col_generate, col_status = st.columns([1, 2])

with col_generate:
    generate_clicked = st.button("Generate Speech", type="primary")

with col_status:
    st.markdown(
        """
        <div class="hint-grid">
            <div class="hint">Latin or Arabic script</div>
            <div class="hint">Browser playback</div>
            <div class="hint">WAV download</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

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
    st.markdown('<div class="audio-box">', unsafe_allow_html=True)
    st.audio(st.session_state.wav_bytes, format="audio/wav")
    st.download_button(
        "Download WAV",
        data=st.session_state.wav_bytes,
        file_name=f"balochi_{st.session_state.last_script_name.lower().replace(' ', '_')}_tts.wav",
        mime="audio/wav",
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown('<div class="audio-box"><div class="empty-audio">&#9835;</div></div>', unsafe_allow_html=True)

if st.session_state.wav_bytes:
    st.markdown('<div class="feedback-box">', unsafe_allow_html=True)
    with st.form("speech_quality_feedback", clear_on_submit=True):
        rating = st.selectbox(
            "Rate the speech quality",
            ["5 - Excellent", "4 - Good", "3 - Average", "2 - Poor", "1 - Very poor"],
        )
        feedback = st.text_input("Feedback message", placeholder="Optional feedback")
        submitted = st.form_submit_button("Submit Rating")

    if submitted:
        save_feedback(
            st.session_state.last_script_name,
            rating,
            feedback,
            st.session_state.last_text,
        )
        st.session_state.rating_submitted = True

    if st.session_state.rating_submitted:
        st.success("Thank you. Your speech quality rating was submitted successfully.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</main>", unsafe_allow_html=True)
