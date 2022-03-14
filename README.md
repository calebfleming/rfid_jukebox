# Setup instructions

<img src=img/components.jpg width="25%" height="25%" /><img src=img/box.jpg width="25%" height="25%" />


## Inspiration
[Phoniebox](http://phoniebox.de/index-en.html)

## Components List
There are many ways to do this, but I ended up using the following components:
- Raspberry Pi 3b
- RC522 RFID module
- Female to male jumper wires
    - Take note of the configuration here based on your Pi internals.
- Soldering equipment
    - This might be optional if your RC522 has the header pins pre-soldered; mine did not
    - Don't let this scare you off; I've never done it before and it was _fine_
    - If you need a very specific shopping list like I did: soldering iron, solder, board to do it on (I used a fireplace brick), and something to clean the solder off of the iron. 
- Mini-breadboard
- Some cheap usb speakers
- Some blank RFID cards
- I used a "Bygglek" lego box from Ikea for the case / decoration

## Necessary Software
- Premium Spotify account
  - In order to use Connect
- Raspotify
    - Turns the Pi into a wifi speaker that's accessible via Spotify Connect
- mfrc522 & spidev
    - For reading and writing RFID cards with your RC522

## Other installations you may have already done
- Python 3.X -- I believe you can run all of this with Python 2... but why?
- I ran everything headless. If you don't know how, Google how to enable ssh, establish a wifi connection, and change the default pi password
- Keep in mind that if you need to install different libraries, do it with the right user (sudo vs root)

## Connecting the components

### RFID reader
I followed [this tutorial](https://pimylifeup.com/raspberry-pi-rfid-rc522/), and it pretty much covers everything from how to physically connect pins from the rfid reader to your breadboard and pi, all the way to actually setting up the python code for installing the reader.

If you need to attach header pins to the RFID reader, there are plenty of soldering tips on YouTube and a few specific to this application as well. See the equipment list above if you've never done it before.

After you have finished the steps in that tutorial, you should be able to run two simple programs.

1. `python3 write_rfid.py` : Asks you for a "card name" to program
2. `python3 read_rfid.py` : Reads the card you programmed and reports back the name and id.

I opted to also use `read_rfid.py` as the entry point for the Spotify integration as well. It ends up containing this logic:
```
- Listen for rfid interactions
- Read the card that was scanned and store the name
- Look up the track uri that corresponds to the card name in mapping dataset
- Check if the currently playing track is the same as the card presented
  - If it's the same, ignore it.
  - If it's different, send a play command
```

### For the Spotify integration:
- Follow the instructions [here](https://github.com/dtcooper/raspotify) for installing Raspotify
- Create a Spotify "client" in Spotify's [developer portal](https://developer.spotify.com/dashboard/applications)
    - You can use the `tokens/tokens.json` file as a reference point for which scopes you will likely need.
- Authorize your user to said client with this url: https://developer.spotify.com/dashboard/applications/your-client-id/users 
- Follow the instructions here to the ["authorization code flow"](https://developer.spotify.com/documentation/general/guides/authorization/code-flow/)
    - For inspiration, look at `src/authorization_setup/authorize.py` , `src/authorization_setup/access_token.py` , and `src/refresh_token.py`. I found this to be the most difficult part of the whole process. But, I basically ran these in order to get the credentials right. And then ...
    - In `tokens/tokens.json` you'll see a skeleton of the file that you need but with my tokens removed.
    - It's a bit lazy but in my code I don't even check for token expiration, I just refresh it every time anyway because the performance is good enough.
- Create a mapping of tracks to cards. Example in `track_mapping.yaml`.
- You need to get the "Spotify" device-id of your pi for a later API call.
    - This is achieved by calling the `/v1/me/player/devices` endpoint. I used `curl` and the Spotify developer docs to do this quickly and outside this process.
    - If you don't want to set your pi as the destination device, you could use a different device id or leave it blank for future commands to affect the _active_ device only.
- Write the code to satisfy your use-case; for me, I wanted to launch with two features:
    1. When a card is touched, play a track
    2. If the card is left on the sensor, don't keep restarting the same track
- I haven't built this yet, but a card that triggers a "pause" command would be nice as a kill switch. I just use my phone and it's fine I guess.
- Expect your recommendations to be ruined if you're building this for a child.

## Final steps

I created a launcher script with these contents:

```
cd /
cd home/pi/lego_jukebox/
sudo python3 read_rfid.py &
```

In order to get my program to run on boot (and before login), I added the launcher before ```exit 0``` in the `/etc/rc.local` file. Ex:

```sudo sh /home/pi/lego_jukebox/launcher.sh```

## Closing comments

I have no idea what I'm doing, which means that you can do it too :) 