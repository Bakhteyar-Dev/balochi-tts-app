import io
import wave

import numpy as np
import streamlit as st
import torch
from transformers import AutoTokenizer, VitsModel


TTS_MODEL_IDS = {
    "Latin Script": "facebook/mms-tts-bcc-script_latin",
    "Arabic Script": "facebook/mms-tts-bcc-script_arabic",
}


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


st.set_page_config(
    page_title="Neurolingo",
    page_icon="audio",
    layout="wide",
)

if "wav_bytes" not in st.session_state:
    st.session_state.wav_bytes = None
if "last_script_name" not in st.session_state:
    st.session_state.last_script_name = None
if "rating_submitted" not in st.session_state:
    st.session_state.rating_submitted = False

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;600;700;800&display=swap');

    :root {
        --ink: #0f172a;
        --muted: #334155;
        --panel: #ffffff;
        --line: #bfddfb;
        --blue: #0b5cad;
        --blue-soft: #eaf6ff;
        --violet: #5941e8;
    }

    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Manrope', sans-serif;
        color: var(--ink);
        background:
            radial-gradient(circle at 8% 16%, rgba(14,165,233,0.15), transparent 28%),
            radial-gradient(circle at 92% 82%, rgba(37,99,235,0.15), transparent 32%),
            linear-gradient(135deg, #ffffff 0%, #f3fbff 46%, #e8f4ff 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 1.8rem;
        padding-bottom: 2rem;
    }

    .hero {
        border-radius: 24px;
        padding: 28px 34px;
        background: rgba(255,255,255,0.92);
        box-shadow: 0 18px 48px rgba(15, 23, 42, 0.08);
        margin-bottom: 22px;
    }

    .hero-inner {
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 28px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 28px;
        background: #ffffff;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 18px;
        min-width: 0;
    }

    .logo {
        width: 82px;
        height: 58px;
        border-radius: 18px;
        display: grid;
        place-items: center;
        color: #ffffff;
        font-size: 29px;
        font-weight: 800;
        background: linear-gradient(135deg, #12a8ef, var(--violet));
        box-shadow: 0 14px 30px rgba(37, 99, 235, 0.18);
    }

    .title {
        margin: 0;
        color: #000000;
        font-size: clamp(34px, 5vw, 46px);
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: 0;
    }

    .subtitle {
        margin-top: 6px;
        color: #111827;
        font-size: 16px;
    }

    .hero-actions {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 16px;
    }

    .chip {
        border-radius: 999px;
        padding: 12px 24px;
        background: var(--blue);
        color: #ffffff;
        font-size: 15px;
        font-weight: 800;
        box-shadow: 0 12px 26px rgba(11, 92, 173, 0.22);
    }

    .script-box {
        border: 1px solid #d7e7f7;
        border-radius: 999px;
        padding: 12px 18px;
        background: #ffffff;
        min-width: 300px;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }

    .script-label {
        color: var(--ink);
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .workspace {
        max-width: 1080px;
        margin: 0 auto;
        border: 1px solid var(--line);
        border-radius: 24px;
        background: rgba(255, 255, 255, 0.56);
        box-shadow: 0 18px 48px rgba(15, 23, 42, 0.08);
        padding: 24px;
    }

    .panel-title {
        display: inline-flex;
        align-items: center;
        border: 1px solid #9ed4ff;
        border-radius: 999px;
        padding: 10px 18px;
        margin-bottom: 12px;
        background: linear-gradient(135deg, #ffffff 0%, var(--blue-soft) 100%);
        color: #000000;
        font-size: 16px;
        font-weight: 800;
    }

    div[data-testid="stTextArea"] label {
        font-weight: 800;
        color: var(--ink);
    }

    div[data-testid="stTextArea"] textarea {
        min-height: 240px;
        border-radius: 18px;
        border: 1px solid #d7e7f7;
        background: #ffffff;
        color: var(--ink);
        font-size: 17px;
        line-height: 1.65;
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.05);
    }

    .stButton > button {
        width: 100%;
        border-radius: 22px;
        border: 0;
        padding: 0.9rem 1rem;
        background: var(--blue);
        color: white;
        font-weight: 800;
        font-size: 18px;
        box-shadow: 0 14px 30px rgba(11, 92, 173, 0.26);
    }

    .stButton > button:hover {
        border: 0;
        color: white;
        background: #084b91;
    }

    .stDownloadButton > button {
        width: 100%;
        border-radius: 16px;
        border: 1px solid #9ed4ff;
        color: var(--blue);
        background: rgba(255,255,255,0.86);
        font-weight: 800;
    }

    .audio-box {
        min-height: 240px;
        border-radius: 18px;
        border: 1px solid #d7e7f7;
        background: #ffffff;
        padding: 20px;
        box-shadow: 0 12px 26px rgba(15, 23, 42, 0.05);
    }

    .empty-output {
        min-height: 196px;
        display: grid;
        place-items: center;
        color: #7b8794;
        font-size: 38px;
    }

    .feedback-box {
        margin-top: 20px;
        border-top: 1px solid #d7e7f7;
        padding-top: 16px;
    }

    div[data-testid="stSelectbox"] label {
        font-weight: 800;
        color: var(--ink);
    }

    @media (max-width: 720px) {
        .block-container {
            padding: 1rem;
        }

        .hero {
            padding: 16px;
        }

        .hero-inner,
        .workspace {
            border-radius: 22px;
            padding: 20px;
        }

        .hero-inner,
        .brand {
            align-items: flex-start;
            flex-direction: column;
        }

        .hero-actions {
            width: 100%;
            align-items: stretch;
        }

        .script-box {
            min-width: 0;
            width: 100%;
        }

        .logo {
            width: 72px;
            height: 52px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
        <div class="hero-inner">
            <div class="brand">
                <div class="logo">NL</div>
                <div>
                    <h1 class="title">Neurolingo</h1>
                    <div class="subtitle">Balochi Text-to-Speech Generator</div>
                </div>
            </div>
            <div class="hero-actions">
                <div class="chip">Text-to-Speech Generator</div>
                <div class="script-box">
                    <div class="script-label">Voice script</div>
                    <div class="script-label">Latin / Arabic</div>
                </div>
            </div>
        </div>
    </section>
    """,
    unsafe_allow_html=True,
)

use_arabic_script = st.toggle(
    "Arabic script",
    value=False,
)

script_name = "Arabic Script" if use_arabic_script else "Latin Script"
script_hint = "Latin-script Balochi text" if script_name == "Latin Script" else "Arabic-script Balochi text"

st.markdown('<main class="workspace">', unsafe_allow_html=True)

input_col, output_col = st.columns(2)

with input_col:
    st.markdown('<div class="panel-title">Balochi Text</div>', unsafe_allow_html=True)
    text = st.text_area(
        f"Enter {script_hint}",
        height=210,
        placeholder=f"Type {script_hint} here...",
        label_visibility="collapsed",
    )

with output_col:
    st.markdown('<div class="panel-title">Balochi Speech</div>', unsafe_allow_html=True)
    st.markdown('<div class="audio-box">', unsafe_allow_html=True)
    if st.session_state.wav_bytes:
        st.audio(st.session_state.wav_bytes, format="audio/wav")
        st.download_button(
            "Download WAV",
            data=st.session_state.wav_bytes,
            file_name=f"balochi_{st.session_state.last_script_name.lower().replace(' ', '_')}_tts.wav",
            mime="audio/wav",
        )
    else:
        st.markdown('<div class="empty-output">&#9835;</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

center_left, center_mid, center_right = st.columns([1, 2, 1])

with center_mid:
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
                st.session_state.rating_submitted = False
                st.rerun()
            except Exception as error:
                st.error(f"Could not generate speech: {error}")

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
        st.session_state.rating_submitted = True

    if st.session_state.rating_submitted:
        st.success("Thank you. Your speech quality rating was submitted successfully.")

    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</main>", unsafe_allow_html=True)
