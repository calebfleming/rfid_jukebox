import requests


def start_playback(self):
    play_endpoint = "https://api.spotify.com/v1/me/player/play"
    play_context = "spotify:track:{}".format(self.NEW_TRACK)

    data = {"uris": [play_context]}
    headers = {'Content-Type': "application/json", 'Authorization': "Bearer " + self.TOKENS["access_token"]}
    query_string = {"device_id": self.DEVICE_ID}

    playback_response = requests.request(
        "PUT",
        url=play_endpoint,
        headers=headers,
        json=data,
        params=query_string
    )

    # validate output
    if (playback_response.status_code == 204) | (playback_response.status_code == 202):
        print("Play command returned successful response")
    else:
        print(playback_response.status_code)
        print("Failure in send_play_command")

    return
