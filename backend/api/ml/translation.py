"""English to Balochi translation inference.

Heavy ML imports (torch / transformers) are done lazily inside the functions so
that Django can start and run management commands without the model stack
installed. Models are cached in-process after the first request.
"""
from functools import lru_cache

from api.constants import TRANSLATION_MODELS

_MAX_LENGTH = 256
_NUM_BEAMS = 4


@lru_cache(maxsize=None)
def _load_model(model_id: str):
    import torch
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_id).to(device)
    model.eval()
    return tokenizer, model, device


def translate(text: str, script: str) -> str:
    """Translate English ``text`` into Balochi for the given ``script``."""
    import torch

    model_id = TRANSLATION_MODELS[script]["id"]
    tokenizer, model, device = _load_model(model_id)

    inputs = tokenizer(
        text, return_tensors="pt", truncation=True, max_length=_MAX_LENGTH
    )
    inputs = {key: value.to(device) for key, value in inputs.items()}

    with torch.no_grad():
        generated = model.generate(
            **inputs, max_length=_MAX_LENGTH, num_beams=_NUM_BEAMS
        )

    return tokenizer.batch_decode(generated, skip_special_tokens=True)[0].strip()
