import requests


def set_repeat_state(self):
    SET_REPEAT = "https://api.spotify.com/v1/me/player/repeat"
    headers = {'Content-Type': "application/json", 'Authorization': "Bearer " + self.TOKENS["access_token"]}
    query_string = {"device_id": self.DEVICE_ID,
                    "state": self.REPEAT_STATE}

    repeat_response = requests.request(
        "PUT",
        url=SET_REPEAT,
        headers=headers,
        params=query_string
    )

    print("Repeat set to {}".format(self.REPEAT_STATE))

    return repeat_response
