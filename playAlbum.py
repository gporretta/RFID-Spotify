#!/usr/bin/env python

import serial
import json
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

# Can't ctrl c out of program without!
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Define the COM port and baud rate
com_port = 'COM3'
baud_rate = 9600

# Open the serial port
ser = serial.Serial(com_port, baud_rate)

albumsJSON = "albums.json"

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'YOUR_CLIENT_ID'
SPOTIPY_CLIENT_SECRET = 'YOUR_CLIENT_SECRET'
SPOTIPY_REDIRECT_URI = 'YOUR_REDIRECT_URI'

sp = Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                       client_secret=SPOTIPY_CLIENT_SECRET,
                                       redirect_uri=SPOTIPY_REDIRECT_URI,
                                       scope="user-read-playback-state,user-modify-playback-state"))

def play_album(uid):

    # Load the JSON 
    with open(albumsJSON, 'r') as file:
        data = json.load(file)

    try:
        # Loop through JSON and see if UID exists
        for item in data:
            if item["uid"] == uid:

                # Get album and artist corresponding to UID in JSON
                album_name = item["album_name"]
                artist_name = item["artist_name"]

                # Get ablum id from spotify
                results = sp.search(q=f"album:{album_name} artist:{artist_name}", type='album')

                # Get top result
                album_id = results['albums']['items'][0]['id']

                # Loop over each result to find exact match
                # else just use top result
                for result in (results['albums']['items']):
                    if result['name'] == album_name:
                        album_id = result['id']
                      
                print("    " + album_id)

                # Get device ID
                devices = sp.devices()
                device_id = devices['devices'][0]['id']  # Get first available device
                print("    " + device_id)

                # Start playback 
                sp.start_playback(device_id=device_id, context_uri='spotify:album:' + album_id)
                print(f"    Playing: {album_name} by {artist_name} \n")
                break
    
    except:
        print(f"    Error Playing: {album_name} by {artist_name} \n")
        return
        
try:
    while True:
        print("Waiting for RFID UID scan:")

        # Read data from the serial port
        uid = ser.readline().decode('utf-8').strip()

        print(f"    Recieved: {uid}")
        play_album(uid)


except KeyboardInterrupt:
    # Close serial port 
    pass

finally:
    # Close serial port 
    ser.close()
