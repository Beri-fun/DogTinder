# DogTinder

The repository contains the project which I did for my university's classes.

The application is based on frame based dialogue system and uses Microsoft Azure API Speech Studio.

DogTinder is an app that helps you navigate the dog matching process through natural conversation. You describe your preferences, apartment size, pets you own and many more and based on that, the best match from among the available dogs is selected.

You communicate only by using your voice.

Additionally, all voice responses (yours and the assistant's) are displayed as text in a dialog box to show the conversation history and allow you to return to previously provided information.

The pretrained resnet50 is used to allow searching for similar dog photos in available set of dogs (for adoption), based on visual appearance.

## Matching criteria

The assistant choose the dog based on: gender, activity level, size, age, coat length, is dog good for children, is dog good with other animals. 

There are also control question about having enough time for a dog, having enough space in home, being prepared for costs and what will happen to a dog if an adopter will go on a vacation.

If any of the control questions are not answered as expected, the dog will not be chosen to a potential adoption and a user will be informed about it.

The assistant is waiting for specific criteria so if during the conversation he does not get it, he will ask again.

Your can also say that some criteria are not important for you and then these will not be considered during matching.

## How does it work?

You talk to the app using your voice – you share your lifestyle, living conditions and dog preferences, such as coat length or preferred gender. The assistant answers you also by voice.

DogTinder analyzes numerous criteria, such as the dog's activity level, size, temperament and care requirements.

He asks additional questions, such as whether you already have any pets at home that the dog will have contact with.

Based on your answers the app searches the database of dogs available for adoption.

You receive a suggested match along with a description of the pet and contact information.

You can also ask assistant to show the similar dog to the selected one based on visual appearance.

After conversation you will be able to see all dogs ready for adoption.

## How to start app
It was run on Ubuntu 22.04 and using Python 3.10.

Set environmental variables *SPEECH_KEY* and *SPEECH_REGION* to use the Microsoft Azure API.
Install requirements specified in```\path\to\this\repo\requirements.txt ``` file.
Start the app:

```
$ \path\to\this\repo> python3 manage.py migrate
$ \path\to\this\repo> python3 manage.py runserver
```

Go to http://localhost:8000/dogTinder/home in your browser and start using the app.

<img width="1919" height="915" alt="photo" src="https://github.com/user-attachments/assets/5f3d701d-e74a-4d66-bdb7-4527b11f97c6" />
<img width="1919" height="915" alt="photo" src="https://github.com/user-attachments/assets/7ba2c3fa-0c1a-4e40-b145-d78d44d297ec" />
<img width="1919" height="915" alt="photo" src="https://github.com/user-attachments/assets/daed7bd3-e3a9-4c74-8657-899d6562c7a9" />
<img width="1919" height="915" alt="photo" src="https://github.com/user-attachments/assets/1933fb2f-9ec1-4f1e-a06c-4dcd30a4131f" />



