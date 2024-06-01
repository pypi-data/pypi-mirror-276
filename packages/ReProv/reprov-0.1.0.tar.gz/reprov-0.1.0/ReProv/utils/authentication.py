import requests
import os

def get_access_token():
    data = {
        "client_id": os.environ['KEYCLOAK_CLIENT_ID'],
        "username": os.environ['KEYCLOAK_USERNAME'],
        "password": os.environ['KEYCLOAK_PASSWORD'],
        "grant_type": "password"
    }

    response = requests.post(os.environ['KEYCLOAK_URL'], data=data)
    access_token = response.json()['access_token']
    return access_token