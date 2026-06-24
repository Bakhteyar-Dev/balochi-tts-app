from rest_framework import serializers

from api.constants import VALID_SCRIPTS


class TranslateSerializer(serializers.Serializer):
    text = serializers.CharField(trim_whitespace=True)
    script = serializers.ChoiceField(choices=VALID_SCRIPTS, default="latin")


class TextToSpeechSerializer(serializers.Serializer):
    text = serializers.CharField(trim_whitespace=True)
    script = serializers.ChoiceField(choices=VALID_SCRIPTS, default="latin")
