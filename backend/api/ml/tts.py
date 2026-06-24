"""Balochi text-to-speech inference using the Facebook MMS VITS models.

Heavy ML imports are done lazily so Django can run without the model stack
installed. Generated audio is returned as in-memory 16-bit PCM WAV bytes.
"""
import io
import wave
from functools import lru_cache

from api.constants import TTS_MODELS

_MAX_LENGTH = 256


@lru_cache(maxsize=None)
def _load_model(model_id: str):
    import torch
    from transformers import AutoTokenizer, VitsModel

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = VitsModel.from_pretrained(model_id).to(device)
    model.eval()
    return tokenizer, model, device


def _waveform_to_wav_bytes(waveform, sampling_rate: int) -> bytes:
    import numpy as np

    waveform = np.clip(waveform, -1.0, 1.0)
    audio_int16 = (waveform * 32767).astype(np.int16)

    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sampling_rate)
        wav_file.writeframes(audio_int16.tobytes())

    return buffer.getvalue()


def synthesize(text: str, script: str) -> bytes:
    """Generate speech for Balochi ``text`` and return WAV bytes."""
    import torch

    model_id = TTS_MODELS[script]["id"]
    tokenizer, model, device = _load_model(model_id)

    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=_MAX_LENGTH
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        waveform = model(**inputs).waveform

    waveform = waveform.squeeze().detach().cpu().numpy()
    return _waveform_to_wav_bytes(waveform, model.config.sampling_rate)
