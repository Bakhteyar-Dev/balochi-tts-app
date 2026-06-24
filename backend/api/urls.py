from django.urls import path

from api import views

urlpatterns = [
    path("health/", views.health, name="health"),
    path("translate/", views.translate, name="translate"),
    path("tts/", views.text_to_speech, name="tts"),
]
