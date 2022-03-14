import requests
import json

def refresh(client_id, client_secret, redirect, token_path):
    # auth urls
    auth_url = 'https://accounts.spotify.com/api/token'

    # read token
    with open(token_path) as json_file:
        tokens = json.load(json_file)

    auth_response = requests.post(auth_url, {
        'grant_type': 'refresh_token',
        'refresh_token': tokens['refresh_token'],
        'redirect_uri': redirect,
        'client_id': client_id,
        'client_secret': client_secret
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    return auth_response_data
