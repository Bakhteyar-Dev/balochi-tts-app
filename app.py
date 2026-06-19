import io
import wave

import numpy as np
import streamlit as st
import torch
from transformers import AutoTokenizer, VitsModel


TTS_MODEL_ID = "facebook/mms-tts-bcc-script_latin"


@st.cache_resource
def load_tts_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(TTS_MODEL_ID)
    model = VitsModel.from_pretrained(TTS_MODEL_ID).to(device)
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


def text_to_speech(text):
    tokenizer, model, device = load_tts_model()

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
    page_title="Balochi Latin Text to Speech",
    page_icon="audio",
    layout="centered",
)

st.title("Balochi Latin Text to Speech")
st.caption("Powered by Balochi Latin text-to-speech")

text = st.text_area(
    "Enter Balochi text in Latin script",
    height=160,
    placeholder="Type Latin-script Balochi text here...",
)

if st.button("Generate Speech", type="primary"):
    clean_text = text.strip()

    if not clean_text:
        st.warning("Please enter Balochi text first.")
    else:
        with st.spinner("Generating speech..."):
            try:
                wav_bytes = text_to_speech(clean_text)
                st.audio(wav_bytes, format="audio/wav")
                st.download_button(
                    "Download WAV",
                    data=wav_bytes,
                    file_name="balochi_latin_tts.wav",
                    mime="audio/wav",
                )
            except Exception as error:
                st.error(f"Could not generate speech: {error}")
