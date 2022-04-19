import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import modules.runner as runner

rfid = SimpleMFRC522()

while True:
    id, text = rfid.read()
    print("Read {text} successfully".format(text=text))
    try:
        p = runner.Playback(str(text))
        p.run()
    except Exception as e:
        print(e)
