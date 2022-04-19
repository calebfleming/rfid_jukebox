import yaml
import time

from modules import refresh_token as refresh_token
from modules import get_currently_playing as gcp
from modules import send_play_command as spc
from modules import set_repeat_state as srs


class Playback:
    def __init__(self, selection):
        self.CRED_PATH = '/home/pi/lego_jqbx/tokens/creds.yaml'
        self.TOKEN_PATH = '/home/pi/lego_jqbx/tokens/tokens.json'
        self.TRACK_PATH = '/home/pi/lego_jqbx/track_mapping.yaml'

        # get creds
        with open(self.CRED_PATH, 'r') as f:
            credentials = yaml.safe_load(f)

        self.CLIENT_ID = credentials['client_id']
        self.CLIENT_SECRET = credentials['client_secret']
        self.REDIRECT_URI = credentials['redirect_uri']
        self.DEVICE_ID = credentials['device_id']

        # get track mapping
        with open(self.TRACK_PATH, 'r') as f:
            track_mapping = yaml.safe_load(f)

        self.selection = selection
        self.NEW_TRACK = track_mapping['rfids'][self.selection.strip()]

        # get clean token
        self.TOKENS = refresh_token.refresh(self)

        # turn off repeat
        self.REPEAT_STATE = "off"

    def get_current_track(self):
        now_track = gcp.now_playing(self)
        if self.NEW_TRACK == now_track:
            print("New track == old track, ignoring command and sleeping for 15s")
            time.sleep(15)
            return True
        else:
            return False

    def start_playback(self):
        spc.start_playback(self)

    def set_repeat_state(self):
        srs.set_repeat_state(self)

    def run(self):
        # check if we need to skip the track
        skip_track = self.get_current_track()
        if skip_track:
            return

        # send the play command
        self.start_playback()

        # set repeat context
        self.set_repeat_state()

        return

