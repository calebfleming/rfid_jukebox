import requests
import yaml
import refresh_token

def now_playing():
    ############################
    # get client id and secret #
    ############################

    with open('/home/pi/lego_jukebox/tokens/creds.yaml', 'r') as f:
        creds = yaml.safe_load(f)

    CLIENT_ID = creds['client_id']
    CLIENT_SECRET = creds['client_secret']
    REDIRECT_URI = creds['redirect_uri']
    TOKEN_PATH = creds['tokens']

    tokens = refresh_token.refresh(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_PATH)

    ###########################
    # check currently playing #
    ###########################

    URI = "https://api.spotify.com/v1/me/player/currently-playing"

    headers = {'Content-Type': "application/json", 'Authorization': "Bearer " + tokens["access_token"]}

    playback_response = requests.request(
        "GET",
        url = URI,
        headers = headers
    )

    if playback_response.status_code == 200:
        output = playback_response.json()
        track_uri = output['item']['uri'].split(':')[2]
        print(track_uri)
    else:
        track_uri = ""

    return track_uri


if __name__ == "__main__":
    now_playing()
