import io
import wave
import re

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
# STYLES
# ----------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Naskh+Arabic:wght@400;500;700&display=swap');

:root {
    --bv-ink: var(--text-color);
    --bv-muted: color-mix(in srgb, var(--text-color) 60%, transparent);
    --bv-border: color-mix(in srgb, var(--text-color) 16%, transparent);
    --bv-bg-soft: var(--secondary-background-color);
    --bv-card-bg: var(--secondary-background-color);
    --bv-purple: #8a5cf0;
    --bv-purple-dark: #6f3fdc;
    --bv-card-radius: 16px;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; color: var(--bv-ink); }
.block-container { padding-top: 3.2rem; max-width: 820px; }

/* ---------- Top bar / logo ---------- */
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
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: normal;
    white-space: nowrap;
}
.bv-brand-name .accent { color: var(--bv-purple); }

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
.st-key-input_card, .st-key-result_card {
    background: var(--bv-card-bg);
    border: 1px solid var(--bv-border);
    border-radius: var(--bv-card-radius);
    padding: 24px 26px 8px 26px;
    margin-bottom: 20px;
}
.st-key-input_card > div, .st-key-result_card > div { gap: 0 !important; }
.bv-section-title { font-size: 1.15rem; font-weight: 700; margin-bottom: 4px; }
.bv-section-caption { font-size: 0.85rem; color: var(--bv-muted); margin-bottom: 18px; }

/* ---------- Segmented script switch ---------- */
.st-key-script_switch {
    max-width: 260px;
    margin: 0 auto 22px auto;
    background: var(--bv-bg-soft);
    border: 1px solid var(--bv-border);
    border-radius: 999px;
    padding: 4px;
}
.st-key-script_switch div[data-testid="stHorizontalBlock"] { gap: 4px; }
.st-key-script_switch button {
    border-radius: 999px !important;
    font-weight: 700 !important;
    border: none !important;
    transition: all 0.15s ease;
}
.st-key-script_switch button[kind="primary"] {
    background: linear-gradient(135deg, #8a5cf0, var(--bv-purple-dark)) !important;
    color: white !important;
    box-shadow: 0 4px 10px rgba(111, 63, 220, 0.3);
}
.st-key-script_switch button[kind="secondary"] {
    background: transparent !important;
    color: var(--bv-muted) !important;
    box-shadow: none !important;
}
.st-key-script_switch button[kind="secondary"]:hover {
    color: var(--bv-ink) !important;
}

/* ---------- Primary action button ---------- */
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, var(--bv-purple), var(--bv-purple-dark));
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.4rem;
    font-weight: 700;
    box-shadow: 0 6px 16px rgba(111, 63, 220, 0.28);
}

/* ---------- Topbar ---------- */
.st-key-topbar { border-bottom: 1px solid var(--bv-border); margin-bottom: 30px; padding-bottom: 14px; }
.st-key-topbar div[data-testid="stHorizontalBlock"] { align-items: center; }

/* ---------- Misc ---------- */
.bv-avg-rating { font-size: 0.85rem; color: var(--bv-muted); margin-top: 6px; }

/* ---------- Mobile responsive fixes ---------- */
@media screen and (max-width: 600px) {

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        padding-top: 3.5rem;
    }

    .st-key-topbar {
        padding-top: 8px;
        padding-bottom: 16px;
        margin-bottom: 24px;
        overflow: visible !important;
    }

    .bv-brand {
        display: flex;
        align-items: center;
        gap: 10px;
        min-height: 48px;
        overflow: visible !important;
    }

    .bv-logo-mark {
        width: 42px;
        height: 42px;
        min-width: 42px;
        min-height: 42px;
        border-radius: 11px;
        overflow: visible !important;
    }

    .bv-brand-name {
        font-size: 1.2rem;
        line-height: 1.2;
    }

    .bv-hero-title {
        font-size: 1.8rem;
        line-height: 1.2;
    }

    .bv-hero-sub {
        font-size: 0.9rem;
        margin-bottom: 20px;
    }

    .st-key-input_card,
    .st-key-result_card {
        padding: 18px 16px 8px 16px;
        border-radius: 14px;
    }

    .st-key-script_switch {
        max-width: 100%;
        width: 100%;
        padding: 5px;
        margin-bottom: 18px;
    }

    .st-key-script_switch div[data-testid="stHorizontalBlock"] {
        display: flex;
        flex-direction: row;
        gap: 6px;
    }

    .st-key-script_switch div[data-testid="column"] {
        width: 50% !important;
        flex: 1 1 0 !important;
        min-width: 0 !important;
    }

    .st-key-script_switch button {
        width: 100% !important;
        min-height: 42px;
        font-size: 0.9rem !important;
        padding: 0.45rem 0.6rem !important;
    }

    div[data-testid="stTextArea"] textarea {
        font-size: 1rem !important;
        min-height: 140px !important;
    }

    div[data-testid="stButton"] button[kind="primary"] {
        min-height: 44px;
        font-size: 0.95rem !important;
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

st.set_page_config(page_title="BakhtAI Voice", page_icon="🎙️", layout="centered")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---- Top bar / logo ----
with st.container(key="topbar"):
    st.markdown(
        f"""
        <div class="bv-brand">
            <div class="bv-logo-mark">{LOGO_SVG}</div>
            <span class="bv-brand-name">Bakht<span class="accent">AI</span> Voice</span>
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
    st.markdown('<div class="bv-section-caption">Switch the script, then type your Balochi text below.</div>', unsafe_allow_html=True)

    # ---- Segmented script switch ----
    with st.container(key="script_switch"):
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

    btn_col1, btn_col2 = st.columns([3, 1])

    with btn_col1:
        generate_clicked = st.button(
            "Generate Speech",
            type="primary",
            use_container_width=True,
            key="btn_generate"
        )

    with btn_col2:
        st.button(
            "Clear",
            use_container_width=True,
            key="btn_clear",
            on_click=clear_input
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
