from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
import os
import subprocess
from DogTinderApp.azure_communication.speech_to_text import recognize_from_microphone
from DogTinderApp.azure_communication.text_to_speech import say_text
from DogTinderApp.DogAssistant import DogAssistant
from DogTinderApp.models import Dog

dogAssistant = DogAssistant()


def home(request):
    return render(request, 'home.html')

def voice_chat(request):
    dogAssistant.reset_frame()
    return render(request, 'voice_chat.html')

def text_to_speech(request):
    if request.method == 'POST':
        text_to_read = request.POST['text'].replace('<br>','')
        say_text(text_to_read)

    return HttpResponse(200)


def speech_to_text(request):
    if request.method == 'POST' and request.FILES['audio']:
        audio_file = request.FILES['audio']
        file_path = os.path.abspath(os.getcwd()) + '/DogTinderApp/static/audio.wav'
        
        with open(file_path, 'wb') as f:
            for chunk in audio_file.chunks():
                f.write(chunk)

    subprocess.run(['bash', 'DogTinderApp/convert.sh'], check=True)

    new_file_path = os.path.abspath(os.getcwd()) + '/DogTinderApp/static/output.wav'

    text_result = recognize_from_microphone(new_file_path)

    os.remove(file_path)
    os.remove(new_file_path)
    return JsonResponse({'text': text_result})

def talk_with_dog_assistant(request):
    user_text = request.POST.get('userMessage', None)
    update, question, photo_name, done = dogAssistant.handle_input(user_input=user_text)
    response = {'text': question,"update":update, "done": done}
    if photo_name is not None:
        response.update({'photo_name': photo_name, 'description': dogAssistant.dog.description})
    return JsonResponse(response)


def reset_conversation(request):
    dogAssistant.reset_frame()
    HttpResponse(200)


def dogs(request):
    dogs = Dog.objects.all()
    return render(request, 'dogs.html', context={"dogs": dogs})