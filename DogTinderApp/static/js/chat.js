
let isLeft = true;

function sendMessage(messageText) {
        const chatBox = document.getElementById('chatBox');

        if (!messageText.trim()) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isLeft ? 'message-left' : 'message-right'}`;

        
        const avatar = document.createElement('img');
        avatar.className = 'avatar';
        avatar.src = isLeft ? "/static/dog_logo.jpg" : "/static/user.jpg"; 

        avatar.alt = 'User Avatar';

        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.innerHTML = messageText;
        messageContent.style.fontSize = '16px';

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(messageContent);

        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        isLeft = !isLeft; 
    }

function sendDogPhoto(data) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-left`;

    const dogImage = document.createElement('img');
    dogImage.className = 'dog_photo';
    dogImage.src = `/static/dogs/${data['photo_name']}`;
    dogImage.alt = 'Dog photo';
    dogImage.style.width = '400px';
    dogImage.style.height = 'auto';

    messageDiv.appendChild(dogImage);
    chatBox.appendChild(messageDiv);
    sendDescriptionMessage(data);
}

function sendDescriptionMessage(data){

    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-left';
    messageDiv.style.display = 'flex';
    messageDiv.style.flexDirection = 'column';
    messageDiv.style.alignItems = 'flex-start';

    const descriptionDiv = document.createElement('div');
    descriptionDiv.className = 'dog-description';
    descriptionDiv.textContent = data['description'];
    descriptionDiv.style.display = 'none';
    
    const toggleButton = document.createElement('button');
    toggleButton.textContent = 'Show description';
    toggleButton.className = 'description-toggle btn btn-primary';
    toggleButton.style.marginTop = '10px';

    toggleButton.addEventListener('click', () => {
        if (descriptionDiv.style.display === 'none') {
            descriptionDiv.style.display = 'block';
            toggleButton.textContent = 'Hide description';
        } else {
            descriptionDiv.style.display = 'none';
            toggleButton.textContent = 'Show description';
        }
    });

    messageDiv.appendChild(descriptionDiv);
    messageDiv.appendChild(toggleButton);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; 

}

function sendWaitingMessage(){

    const chatBox = document.getElementById('chatBox');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message message-left';
    messageDiv.id = 'waiting_message'

    
    const avatar = document.createElement('img');
    avatar.className = 'avatar';
    avatar.src =  "/static/dog_logo.jpg"; 
    avatar.alt = 'User Avatar';

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.innerHTML =`<i class="fa-solid fa-ellipsis fa-bounce"></i>`;
    messageContent.style.fontSize = '16px';

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);

    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight; 
}

function showDogsButton(){
    let button = $('#dogs');
    let button2 = $('#webPage')
    $(button).removeClass('d-none');
    $(button2).removeClass('d-none');
}

function getAnswer(userMessage){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append('userMessage', userMessage);
    $.ajax({
        url: 'talk_with_dog_assistant',
        type: 'POST',
        data: formData,
        processData: false,  
        contentType: false,  
        success: function(data) {
            deleteWaitingMessage()
            sendMessage(data['text']);
            if (data['photo_name']){
                showDogsButton()
                sendDogPhoto(data)
            }
            if (data['done']){
                showDogsButton()
            }
            sayMessage(data['text'])
            change_micro_to_be_ready()
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });

}

function sayMessage(message){
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", csrfToken);
    formData.append('text', message,);
    $.ajax({
        url: 'text_to_speech',
        type: 'POST',
        data: formData,
        processData: false,  
        contentType: false,  
        success: function() {
            console.log('Success');
        },
        error: function(error) {
            console.error('Error:', error);
        }
    });
}

function deleteWaitingMessage(update){
    var element = document.getElementById("waiting_message");
    element.parentNode.removeChild(element);
                
    isLeft = true
}