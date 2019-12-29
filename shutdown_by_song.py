#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Helper script, that allows to shutdown the system by playing a song containing "Shutdown"

import mpd
import time
from threading import Thread
import os

# Connect with MPD
client = mpd.MPDClient()


def do_connect():
    connected = False
    while connected == False:
        connected = True
        try:
             client.connect("localhost","6600")
        except SocketError as e:
             connected = False
        if connected == False:
                print("Couldn't connect. Retrying...")
                time.sleep(5)
    print("Connected!")


def connection_status():
    """
    pings server every 60 seconds and prints.
    """
    while True:
        print("pinging the server")
        try:   
            client.ping()
        except (mpd.ConnectionError, OSError) as e:
            do_connect()
        time.sleep(60)


def check_song():
    time.sleep(10)
    while True:
        current_song = client.currentsong()
        if 'file' in current_song and ("Shutdown" in current_song['file'] or "shutdown" in current_song['file']):
            # Prevent from shutting down after startup
            client.next()
            time.sleep(0.1)
            print("Shutting down")
            os.system("sudo shutdown now")
        #else:
        #    print(current_song)
        time.sleep(1)


do_connect()

connect_thread = Thread(target = connection_status)
check_song_thread = Thread(target = check_song)

connect_thread.start()
check_song_thread.start()
