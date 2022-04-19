import requests


def now_playing(self):
    URI = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {'Content-Type': "application/json", 'Authorization': "Bearer " + self.TOKENS["access_token"]}

    playback_response = requests.request("GET", url=URI, headers=headers)

    if playback_response.status_code == 200:
        output = playback_response.json()
        track_uri = output['item']['uri'].split(':')[2]

        # if paused, start playing
        if not output['is_playing']:
            return ""
        elif output['is_playing']:
            return track_uri
        return track_uri
