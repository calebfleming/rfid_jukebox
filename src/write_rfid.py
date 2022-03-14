import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    text = input('Name this card:')
    print("Now place your tag to write")
    reader.write(text)
    print("{} was written".format(text))
finally:
    GPIO.cleanup()
