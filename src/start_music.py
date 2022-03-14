import requests
import yaml
import refresh_token
import get_currently_playing
import time


def launch_playback(selection):

    ##########################
    # read the mapping table #
    ##########################

    with open('/home/pi/lego_jukebox/track_mapping.yaml', 'r') as f:
        doc = yaml.safe_load(f)

    TRACK_SELECTION = doc['rfids'][selection.strip()]
    CURRENT_TRACK = get_currently_playing.now_playing()

    if TRACK_SELECTION == CURRENT_TRACK:
        print("track is already playing, ignore")
        time.sleep(30)
        return

    ############################
    # get client id and secret #
    ############################

    with open('/home/pi/lego_jukebox/tokens/creds.yaml', 'r') as f:
        creds = yaml.safe_load(f)

    CLIENT_ID = creds['client_id']
    CLIENT_SECRET = creds['client_secret']
    REDIRECT_URI = creds['redirect_uri']
    DEVICE_ID = creds['device_id']
    TOKEN_PATH = creds['tokens']

    tokens = refresh_token.refresh(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_PATH)

    ###########################
    # push playback to device #
    ###########################

    play_endpoint = "https://api.spotify.com/v1/me/player/play"
    play_context = "spotify:track:{}".format(TRACK_SELECTION)

    data = {"uris": [play_context]}
    headers = {'Content-Type': "application/json", 'Authorization': "Bearer " + tokens["access_token"]}
    query_string = {"device_id": DEVICE_ID}

    playback_response = requests.request(
        "PUT",
        url=play_endpoint,
        headers=headers,
        json=data,
        params=query_string
    )

    # validate output
    if (playback_response.status_code == 204) | (playback_response.status_code == 202):
        print("success")
    else:
        print(playback_response.status_code)
        print("fail!")

    return
