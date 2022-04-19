import requests
import json


def refresh(self):
    # read token
    with open(self.TOKEN_PATH) as json_file:
        tokens = json.load(json_file)

    response = requests.post(
      'https://accounts.spotify.com/api/token',
      {'grant_type': 'refresh_token',
       'refresh_token': tokens['refresh_token'],
       'redirect_uri': self.REDIRECT_URI,
       'client_id': self.CLIENT_ID,
       'client_secret': self.CLIENT_SECRET}
    ).json()

    return response
