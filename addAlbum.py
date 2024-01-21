#!/usr/bin/env python

import os
import json
import serial
import serial.tools.list_ports

# Can't ctrl c out of program without!
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Define the COM port and baud rate
com_ports = serial.tools.list_ports.comports()
for port in com_ports:
        if port.description.__contains__("USB-SERIAL CH340"):
            com_port = port.device
            
baud_rate = 9600

# Open the serial port
ser = serial.Serial(com_port, baud_rate)

albumsJSON = "albums.json"

# Get user input for album details
def get_album_details():
    album_name = input("Enter Album Name: ")
    artist_name = input("Enter Artist Name: ")
    return {"album_name": album_name, "artist_name": artist_name}

# Write data to JSON 
def write_to_json(album_data, filename):
    # Check if JSON already exists
    if os.path.exists(filename):
        # If file exists, load JSON 
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

        #For each entry in JSON see if UID already exists
        for index, entry in enumerate(data):
            # If UID does already exist
            if entry["uid"] == album_data["uid"]:
                # Prompt user and determine result
                overwrite = input("UID already exists. Do you want to overwrite the current entry? (y/n): ").lower()

                # Overwrite album data
                if overwrite == 'y':
                    data[index] = album_data
                    with open(filename, 'w') as json_file:
                        json.dump(data, json_file, indent=2)
                    print("Album overwritten successfully.")
                    return

                # Go back to waiting for RFID scan
                elif overwrite == 'n':
                    print("Album not overwritten.")
                    return
        
        # If UID is unique add new entry with album_data to the list
        data.append(album_data)
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print("New album added successfully.")
            
try:
    while True:
        print("Waiting for RFID UID")

        # Read data from the serial port
        uid = ser.readline().decode('utf-8').strip()

        print(f"Recieved: {uid}")

        # Ask the user for album details
        album_data = get_album_details()

        # Append recieved UID to album_data
        album_data["uid"] = uid

        # Write album_data to JSON file
        write_to_json(album_data, albumsJSON)
        
except KeyboardInterrupt:
    # Close serial port 
    pass

finally:
    # Close serial port 
    ser.close()
