let mediaRecorder;
let audioChunks = [];

function startRecording(){

    audioChunks = [];
    audioBlob = null;
    
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);

            mediaRecorder.ondataavailable = function(event) {
                audioChunks.push(event.data);
            };

            mediaRecorder.onstop = function() {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                sendAudioToServer(audioBlob);
            };

            mediaRecorder.start();

        });
};


function sendAudioToServer(audioBlob) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append('audio', audioBlob, 'audio.wav');
    
    $.ajax({
        url: 'speech_to_text',
        type: 'POST',
        data: formData,
        processData: false,  
        contentType: false,  
        success: function(data) {
            sendMessage(data['text'])
            sendWaitingMessage()
            getAnswer(data['text'])
            
        },
        error: function(error) {
            sendWaitingMessage()
        }
    });
}

function change_micro_to_recording(){
    let micro = $('#recording_button');
    $(micro).html('<i class="fa-solid  fa-lg fa-microphone fa-beat-fade"></i>');
    $(micro).attr('class', "btn btn-primary btn-lg");
    $(micro).attr('data-recording', "recording");
}

function change_micro_to_be_ready(){
    let micro = $('#recording_button');
    $(micro).html('<i class="fa-solid  fa-lg fa-microphone"></i>');
    $(micro).attr('class', "btn btn-primary btn-lg");
    $(micro).attr('data-recording', "ready");
}

function change_micro_to_waiting(){
    let micro = $('#recording_button');
    $(micro).html('<i class="fa-solid  fa-lg fa-microphone"></i>');
    $(micro).attr('class', "btn btn-secondary btn-lg");
    $(micro).attr('data-recording', "waiting");
    
}


$(document).ready(function() {
    firstMessage = "Hi! I'm an assistant who will help you find your perfect furry friend! <br> Adopting a dog is a big decision, so I'll ask you to answer a few questions to make sure we match you with the perfect partner. Shall we get started? <br> Click the microphone icon to tell me what kind of dog you're looking for."
    sendMessage(firstMessage);
    sayMessage(firstMessage)

    $('#recording_button').click(function() {

        if ($(this).attr('data-recording') == 'recording'){
            change_micro_to_waiting()
            mediaRecorder.stop();

        } 
        if ($(this).attr('data-recording') == 'ready'){
            change_micro_to_recording()
            startRecording();
        }
        
    
        
    });

});