import io
import wave
import re

import numpy as np
import streamlit as st
import torch
from transformers import AutoTokenizer, VitsModel

from bv_ui import inject_theme, render_footer, render_sidebar, render_topbar

# ----------------------------------------------------------------------------
# CONFIG
# ----------------------------------------------------------------------------

MODELS = {
    "latin": {
        "id": "facebook/mms-tts-bcc-script_latin",
        "label": "Latin",
        "placeholder": "Type Latin-script Balochi text here... (e.g. Man wati zobáná gapp janán)",
        "direction": "ltr",
        "align": "left",
        "font": "'Inter', sans-serif",
    },
    "arabic": {
        "id": "facebook/mms-tts-bcc-script_arabic",
        "label": "Arabic",
        "placeholder": "\u200eType arabic-script Balochi text here\n\u200f(e.g. من ءَ بلوچی زبان دوست بیت)",
        "direction": "rtl",
        "align": "right",
        "font": "'Noto Naskh Arabic', serif",
    },
}

STAR_LABELS = ["Poor", "Fair", "Good", "Very Good", "Excellent"]

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
# TEXT SCRIPT VALIDATION
# ----------------------------------------------------------------------------

def contains_arabic_script(text: str) -> bool:
    return bool(re.search(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]", text))


def contains_latin_script(text: str) -> bool:
    return bool(re.search(r"[A-Za-z]", text))

# ----------------------------------------------------------------------------
# CLEAR INPUT
# ----------------------------------------------------------------------------

def clear_input():
    st.session_state["bv_text_input"] = ""
    st.session_state.result = None

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

st.set_page_config(page_title="Bakhteyar-AI Voice", page_icon="🎙️", layout="centered")
inject_theme()
render_sidebar()
render_topbar("Voice")

# ----------------------------------------------------------------------------
# HERO
# ----------------------------------------------------------------------------

st.markdown('<span class="bv-eyebrow">Balochi → Speech</span>', unsafe_allow_html=True)

st.markdown(
    '<div class="bv-hero-title">Text to <span class="grad">Speech</span></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="bv-hero-sub">
        Type Balochi text in Latin or Arabic script and generate natural-sounding speech
        in Balochi.
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# INPUT CARD
# ----------------------------------------------------------------------------

with st.container(key="input_card"):
    st.markdown('<div class="bv-section-title">Enter your text</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="bv-section-caption">Switch the script, then type your Balochi text below.</div>',
        unsafe_allow_html=True,
    )

    with st.container(key="script_switch"):
        sw_col1, sw_col2 = st.columns(2)

        with sw_col1:
            if st.button(
                "Balochi-Latin",
                type="primary" if st.session_state.script_key == "latin" else "secondary",
                use_container_width=True,
                key="btn_latin",
            ):
                st.session_state.script_key = "latin"
                st.rerun()

        with sw_col2:
            if st.button(
                "Balochi-Arabic",
                type="primary" if st.session_state.script_key == "arabic" else "secondary",
                use_container_width=True,
                key="btn_arabic",
            ):
                st.session_state.script_key = "arabic"
                st.rerun()

    script_choice = st.session_state.script_key
    current = MODELS[script_choice]

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

    btn_col1, btn_col2 = st.columns([3, 1])

    with btn_col1:
        generate_clicked = st.button(
            "Generate Speech",
            type="primary",
            use_container_width=True,
            key="btn_generate",
        )

    with btn_col2:
        st.button(
            "Clear",
            use_container_width=True,
            key="btn_clear",
            on_click=clear_input,
        )

# ----------------------------------------------------------------------------
# GENERATION
# ----------------------------------------------------------------------------

if generate_clicked:
    clean_text = text.strip()

    if not clean_text:
        st.warning("Please enter Balochi text first.")

    elif script_choice == "latin" and contains_arabic_script(clean_text):
        st.warning("Please select Latin script.")

    elif script_choice == "arabic" and contains_latin_script(clean_text):
        st.warning("Please select Arabic script.")

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

    with st.container(key="result_card"):
        st.markdown('<div class="bv-section-title">Result</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="bv-section-caption">{MODELS[result["script"]]["label"]} script</div>',
            unsafe_allow_html=True,
        )

        st.audio(result["wav"], format="audio/wav")

        st.download_button(
            "Download WAV",
            data=result["wav"],
            file_name=f"bakhtai_voice_{result['script']}.wav",
            mime="audio/wav",
            use_container_width=True,
        )

        st.markdown(
            '<div class="bv-section-title" style="font-size:0.95rem; margin-top:20px;">Rate this audio</div>',
            unsafe_allow_html=True,
        )

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
                st.session_state.feedback_log.append(
                    STAR_LABELS.index(rating_label) + 1
                )
                st.session_state.result["rated"] = True
                st.toast(f"Thanks for rating it {rating_label}!", icon="⭐")

        if st.session_state.feedback_log:
            avg = sum(st.session_state.feedback_log) / len(st.session_state.feedback_log)

            st.markdown(
                f'<div class="bv-avg-rating">Average rating: {avg:.1f} / 5 '
                f'from {len(st.session_state.feedback_log)} rating(s)</div>',
                unsafe_allow_html=True,
            )

render_footer()
