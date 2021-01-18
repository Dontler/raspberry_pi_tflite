import os
import requests


def send_image(path, email):
    with open(os.getcwd() + path, 'rb') as image:
        files = {'photo': image}
        data = {'email': email}
        response = requests.post('http://localhost/mail/send_photo', files=files, data=data)
        response_data = response.json()
        print(response_data['message'])
