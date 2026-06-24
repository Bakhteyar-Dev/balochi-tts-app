"""Shared model configuration for the Balochi language tools."""

TRANSLATION_MODELS = {
    "latin": {
        "id": "Bakhteyar/Balochi-Model",
        "label": "Latin",
        "direction": "ltr",
    },
    "arabic": {
        "id": "Bakhteyar/mbart-en-to-bal-19k",
        "label": "Arabic",
        "direction": "rtl",
    },
}

TTS_MODELS = {
    "latin": {
        "id": "facebook/mms-tts-bcc-script_latin",
        "label": "Latin",
        "direction": "ltr",
    },
    "arabic": {
        "id": "facebook/mms-tts-bcc-script_arabic",
        "label": "Arabic",
        "direction": "rtl",
    },
}

VALID_SCRIPTS = ("latin", "arabic")
