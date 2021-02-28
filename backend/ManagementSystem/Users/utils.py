import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

try:
    from mail_settings import *
except:
    pass

def send_mail(data):
    url = "https://api.sendinblue.com/v3/smtp/email"

    payload = {
        "sender": {
            "name": "Tester",
            "email": SENDER
        },
        "to": [{"email": data['recipient']}],
        "subject": data['subject'],
        "textContent": data['body']
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "api-key": API_KEY
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    print(response.text)

