#!/usr/bin/env python
# -*- coding: utf8 -*-

"""MFRC522-listener for droPlay - selects music based on RFID UID."""

import RPi.GPIO as GPIO
import MFRC522
import signal
import Music
import time

from termcolor import colored

# Import Django-DB:
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "droPlayWeb.settings")
import django
django.setup()

from musiControl.models import Album
droplets = Album.objects.all()

music = Music.Music()
music.root = '/home/pi/Music/'

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending.")
    continue_reading = False
    GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

print
print ("Waiting for drop. Press Ctrl-C to stop.")
print

# Loop checking for RFID-chips:
while continue_reading:
    
    # Scan for droplets
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Found one?
    if status == MIFAREReader.MI_OK:
        print

        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            dropID = ''.join( map(str, uid) )
            print ("Droplet UID: " + dropID)

            match = 0
            for droplet in droplets:
                if str(droplet.dropletID) == dropID:
                    match = 1
                    if not (music.state == 'play' and music.path == droplet.path):
                    	music.play( droplet )

            if not match:
                print ("I don't know this tag")

        else:
            print "Error reading droplet!"

    time.sleep(0.2)

    #else:
        # Maybe pause if last play is some secs ago?
