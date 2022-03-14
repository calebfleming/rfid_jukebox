import requests
import json
import yaml

# get client id and client secret
with open('/home/pi/lego_jukebox/tokens/creds.yaml', 'r') as f:
    creds = yaml.load(f)

CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']
REDIRECT_URI = creds['redirect_uri']
SCOPES = 'user-read-playback-state user-modify-playback-state user-read-currently-playing streaming'

# auth urls
login_url = 'https://accounts.spotify.com/authorize'

response = requests.get(login_url, {'response_type': 'code',
    'client_id': CLIENT_ID,
    'redirect_uri': REDIRECT_URI,
    'scope': SCOPES,
    'show_dialog': True})

print(response.url)

# take this url to your browser and get the "code" after you authenticate. Use this in access_token.py