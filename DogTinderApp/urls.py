from django.urls import path

from . import views

urlpatterns = [
    path("home", views.home, name="home"),
    path("voiceChat", views.voice_chat, name="voice_chat"),
    path("speech_to_text", views.speech_to_text, name="speech_to_text"),
    path("text_to_speech", views.text_to_speech, name="text_to_speech"),
    path("talk_with_dog_assistant", views.talk_with_dog_assistant, name="talk_with_dog_assistant"),
    path("reset_conversation", views.reset_conversation, name="reset_conversation"),
    path("dogs", views.dogs, name="dogs"),
]