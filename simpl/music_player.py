# -*- coding: utf-8 -*-
"""
Abstraction to python-mpd2 for communication with MPD.

Created on Thu Jan 19 21:41:17 2017.

@author: mb

"""
import mpd
import logging


class MusicPlayer(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._client = mpd.MPDClient()
        # network timeout in seconds (floats allowed), default: None
        self._client.timeout = 10
        # timeout for fetching the result of the idle command is handled
        # seperately, default: None
        self._client.idletimeout = None
        self._client.connect("localhost", 6600)
        self._logger.debug("Connected to MPD " + self._client.mpd_version)

    def play(self):
        """Play track"""
        self._client.play(0)

    def pause(self):
        """Pause playing"""
        self._client.pause()

    def play_next(self):
        """Play next song"""
        self._client.next()

    def play_previous(self):
        """Play previous song"""
        self._client.previous()
        
    def clear_playlist(self):
        self._client.clear()

    def switch_to_folder(self, folder):
        """Change folder"""
        self._client.add(folder)
        self.play()

    def get_directories(self):
        root_dirs = self._client.lsinfo()
        dir_list = list()
        for dir in root_dirs:
            if 'directory' in dir:
                 dir_list.append(dir['directory'])
        return(dir_list)

    def __del__(self):
        self._client.close()
        self._client.disconnect()


if __name__ == "__main__":
    music_player = MusicPlayer()
    music_player.get_directories()
    del(music_player)
