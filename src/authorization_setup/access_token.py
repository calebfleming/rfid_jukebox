import requests
import yaml
import json

# get client id and client secret
with open('/home/pi/lego_jukebox/tokens/creds.yaml', 'r') as f:
    creds = yaml.load(f)

CLIENT_ID = creds['client_id']
CLIENT_SECRET = creds['client_secret']
REDIRECT_URI = creds['redirect_uri']
TOKEN_PATH = creds['tokens']
CODE = "enter the code from your browser"

# auth urls
auth_url = 'https://accounts.spotify.com/api/token'

auth_response = requests.post(auth_url, {
    'grant_type': 'authorization_code',
    'redirect_uri': REDIRECT_URI,
    'code': CODE,
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
})

# convert the response to JSON
auth_response_data = auth_response.json()
print(auth_response_data)

# write tokens to file
with open(TOKEN_PATH, 'w') as outfile:
    json.dump(auth_response_data, outfile)
