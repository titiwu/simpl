# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:41:17 2017

@author: mb
"""
import mpd
import logging

class MusicPlayer(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._client = mpd.MPDClient()               # create client object
        self._client.timeout = 10                # network timeout in seconds (floats allowed), default: None
        self._client.idletimeout = None          # timeout for fetching the result of the idle command is handled seperately, default: None
        self._client.connect("localhost", 6600)  # connect to localhost:6600
        self._logger.debug(self._client.mpd_version)          # print the MPD version
        
    def play(self):
        self._client.play(1)
        
    def pause(self):
        self._client.pause()
        
    def playNext(self):
        self._client.next()
        
    def playPrevious(self):
        self._client.previous()
        
    def switchToFolder(self, folder):
        self._client.clear()
        self._client.add(folder)
        self.play()

    def __del__(self):
        self._client.close()                     # send the close command
        self._client.disconnect()                # disconnect from the server
