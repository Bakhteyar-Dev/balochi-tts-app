import base64
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.constants import TRANSLATION_MODELS, TTS_MODELS
from api.serializers import TextToSpeechSerializer, TranslateSerializer

_ARABIC_RE = re.compile(
    r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]"
)
_LATIN_RE = re.compile(r"[A-Za-z]")


@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})


@api_view(["POST"])
def translate(request):
    serializer = TranslateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    text = serializer.validated_data["text"].strip()
    script = serializer.validated_data["script"]

    if not text:
        return Response(
            {"detail": "Please enter English text first."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    from api.ml.translation import translate as run_translation

    try:
        result = run_translation(text, script)
    except Exception as error:  # noqa: BLE001 - surface model errors to client
        return Response(
            {"detail": f"Could not translate text: {error}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    return Response(
        {
            "text": result,
            "script": script,
            "label": TRANSLATION_MODELS[script]["label"],
            "direction": TRANSLATION_MODELS[script]["direction"],
        }
    )


@api_view(["POST"])
def text_to_speech(request):
    serializer = TextToSpeechSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    text = serializer.validated_data["text"].strip()
    script = serializer.validated_data["script"]

    if not text:
        return Response(
            {"detail": "Please enter Balochi text first."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if script == "latin" and _ARABIC_RE.search(text):
        return Response(
            {"detail": "Arabic-script text detected. Please select Arabic script."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if script == "arabic" and _LATIN_RE.search(text):
        return Response(
            {"detail": "Latin-script text detected. Please select Latin script."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    from api.ml.tts import synthesize

    try:
        wav_bytes = synthesize(text, script)
    except Exception as error:  # noqa: BLE001 - surface model errors to client
        return Response(
            {"detail": f"Could not generate speech: {error}"},
            status=status.HTTP_502_BAD_GATEWAY,
        )

    audio_b64 = base64.b64encode(wav_bytes).decode("ascii")
    return Response(
        {
            "audio_base64": audio_b64,
            "mime_type": "audio/wav",
            "script": script,
            "label": TTS_MODELS[script]["label"],
        }
    )
