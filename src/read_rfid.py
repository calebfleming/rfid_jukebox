import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from start_music import launch_playback

rfid = SimpleMFRC522()

while True:
    id, text = rfid.read()
    try:
        launch_playback(str(text))
    except:
        print("Card not programmed and/or mapped to Spotify track uri")
