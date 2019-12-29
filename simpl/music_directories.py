# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 22:23:47 2017

@author: mb
"""
import re
import logging


class SimplDirectories(object):
    """SimplDirectories manages the music directories for simpl."""
    _directories = dict()

    def __init__(self, directory_list):
        self._logger = logging.getLogger(__name__)
        self.process_directories(directory_list)

    def folder_exists(self, folder_number):
        if folder_number in self._directories:
            return True
        else:
            return False

    def get_text_for_folder(self, folder_number):
        if self.folder_exists(folder_number):
            return self._directories[folder_number].dir_text
        else:
            return 'Nichts hinterlegt'

    def get_folder_uri_for_mpd(self, folder_number):
        if self.folder_exists(folder_number):
            return self._directories[folder_number].dir_fullname
        else:
            return ''

    def get_nr_of_folder_entries(self, folder_number):
        if self.folder_exists(folder_number):
            return self._directories[folder_number].nr_of_entries
        else:
            return 0

    def is_radio_folder(self, folder_number):
        """Returns if a given folder contains radio playlists"""
        if self.folder_exists(folder_number):
            return self._directories[folder_number].is_radio
        else:
            return False

    def get_radio_playlist_text(self, folder_number, playlist_nr):
        """Returns text for the radio playlist (e.g. radio station)"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_radio_name(playlist_nr)
        else:
            return 'Fehler'

    def get_radio_uri_for_mpd(self, folder_number, playlist_nr):
        """Returns the URI needed to add the radio-playlist to the mpd playlist"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_full_radio_uri(playlist_nr)
        else:
            return ''

    def get_next_radio_playlist_nr(self, folder_number, playlist_nr):
        """Get next playlist"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_next_playlist_number(playlist_nr)
        else:
            return 0

    def get_previous_radio_playlist_nr(self, folder_number, playlist_nr):
        """Get previous playlist"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_previous_playlist_number(playlist_nr)
        else:
            return 0

    def process_directories(self, directory_list):
        pattern = re.compile("^([0-9]+)-(.*)")
        for directory in directory_list:
            if 'directory' in directory:
                dir_name = directory['directory']
            else:
                self._logger.warn('Faulty information from music player, missing directory name')
                continue
            if (not 'files' in directory) or (not 'playlists' in directory):
                self._logger.warn('Faulty information from music player, missing files or playlist information')
                continue
            # Only recognize folders with "XX-foldername" naming
            # e.g. "02-My_Album"
            if pattern.fullmatch(dir_name):
                search = pattern.search(dir_name)
                dir_number = int(search.group(1))
                dir_text = search.group(2)
                dir_text = dir_text.replace("-", " ")
                dir_text = dir_text.replace("_", " ")
                dir_text = dir_text.strip()
                self._directories[dir_number] = MusicFolder(dir_text, dir_name, directory['files'],
                                                            directory['playlists'])
        self._logger.info(str(len(self._directories)) + ' simpl directories found')


class MusicFolder(object):
    """Music folder properties."""
    is_radio = False
    dir_text = ""
    dir_fullname = ""
    nr_of_entries = 0
    radio_playlists = list()

    def __init__(self, dir_text, dir_fullname, file_names, playlists):
        self._logger = logging.getLogger(__name__)
        self.dir_text = dir_text
        self.dir_fullname = dir_fullname
        if not playlists:
            self.is_radio = False
            self.nr_of_entries = len(file_names)
        else:
            self.is_radio = True
            # save radio Playlist texts in dict
            self.radio_playlists = playlists
            self.nr_of_entries = len(playlists)

    def get_full_radio_uri(self, playlist_nr):
        if playlist_nr < 0 or playlist_nr > len(self.radio_playlists):
            self._logger.info('Playlist nr' + str(playlist_nr) + 'not in directory' + self.dir_fullname)
            return ''
        return self.dir_fullname + '/' + self.radio_playlists[playlist_nr]

    def get_radio_name(self, playlist_nr):
        if playlist_nr < 0 or playlist_nr > len(self.radio_playlists):
            self._logger.info('Playlist nr' + str(playlist_nr) + 'not in directory' + self.dir_fullname)
            return "Fehler"
        return self.radio_playlists[playlist_nr].split('.', 1)[0].replace("_", " ").replace("-", " ")

    def get_next_playlist_number(self, act_nr):
        """Return next number in playlist, wrapping round"""
        if self.nr_of_entries == 0:
            return 0
        else:
            return (act_nr + 1) % (self.nr_of_entries + 1)

    def get_previous_playlist_number(self, act_nr):
        """Return previous number in playlist, wrapping round"""
        if self.nr_of_entries == 0:
            return 0
        else:
            return (act_nr - 1) % (self.nr_of_entries + 1)
