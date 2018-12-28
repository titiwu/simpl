# -*- coding: utf-8 -*-
"""
Abstraction to python-mpd2 for communication with MPD.

Created on Thu Jan 19 21:41:17 2017.

@author: mb

"""
import mpd
import logging
import time


class MusicPlayer(object):
    _act_folder = ''
    _act_song_nr = 0
    _last_scan_time = 0

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

    def get_status(self):
        """ Get the status update, but only when not done in the last 20 Seconds"""
        if self._last_scan_time + 20 < time.time():
            mpd_status = self._client.currentsong()
            if 'pos' in mpd_status:
                self._act_song_nr = int(mpd_status['pos'])
            else:
                self._act_song_nr = 0
            if 'file' in mpd_status:
                self._act_folder = mpd_status['file'].split('/', 1)[0]
            else:
                self._act_folder = ''

    def get_act_song_nr(self):
        self.get_status()
        return self._act_song_nr

    def get_act_folder(self):
        self.get_status()
        return self._act_folder

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
        self._client.clear()
        self._client.add(folder)
        self.play()

    def switch_to_playlist(self, playlist):
        """Change folder"""
        self._client.clear()
        self._client.load(playlist)
        self.play()

    def set_volume(self, volume_prc):
        """Set the playback volume (0-100)"""
        self._client.setvol(volume_prc)

    def get_directories(self):
        """Get directory information for simpl"""
        root_dirs = self._client.lsinfo()
        dir_list = list()
        for dir in root_dirs:
            if 'directory' in dir:
                self._client.lsinfo(dir['directory'])
                file_list = self.get_files(dir['directory'], 'file')
                playlist_list = self.get_files(dir['directory'], 'playlist')
                dir_list.append({'directory': dir['directory'], 'files': file_list, 'playlists': playlist_list})
        return (dir_list)

    def get_files(self, directory, type):
        files = self._client.lsinfo(directory)
        file_list = list()
        for dir in files:
            if type in dir:
                file_list.append(dir[type].replace(directory + '/', ''))
        return (file_list)

    def __del__(self):
        self._client.close()
        self._client.disconnect()


if __name__ == "__main__":
    music_player = MusicPlayer()
    print(music_player.get_directories())
    print(music_player._client.status())
    print(music_player.get_act_song_nr())
    print(music_player.get_act_folder())
    # print(music_player.switch_to_playlist('04-Radio/bayern_2.m3u'))
    del (music_player)
