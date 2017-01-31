# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 22:23:47 2017

@author: mb
"""
import re
import logging


class SimplDirectories(object):
    """SimplDirectories mages the music directories for simpl."""
    _directories = dict()
    
    def __init__(self,  directory_names):
        self._logger = logging.getLogger(__name__)
        self.process_directories(directory_names)
        
    def folder_exists(self,  folder_number):
        if  folder_number in self._directories:
            return True
        else:
            return False

    def get_text_for_folder(self,  folder_number):
        if  self.folder_exists(folder_number):
            return(self._directories[folder_number].dir_text)
        else:
            return ''

    def get_folder_uri_for_mpd(self, folder_number):
        if  self.folder_exists(folder_number):
            return(self._directories[folder_number].dir_fullname)
        else:
            return ''

    def process_directories(self,  directory_names):
        pattern = re.compile("^([0-9]+)-(.*)")
        for dir_name in directory_names:
            if pattern.fullmatch(dir_name):
                search = pattern.search(dir_name)
                dir_number = int(search.group(1))
                dir_text = search.group(2)
                dir_text = dir_text.replace("-", " ")
                dir_text = dir_text.replace("_", " ")
                dir_text = dir_text.strip()
                self._directories[dir_number] = MusicFolder(dir_text,  dir_name,  [])
        self._logger.info(str(len(self._directories)) +'simpl directories found')

class MusicFolder(object):
    """Music folder properties."""
    is_radio = False
    dir_text = ""
    dir_fullname = ""
    nr_of_entries = 0
    radio_playlists = dict()
    
    def __init__(self,  dir_text,  dir_fullname,  playlists):
        self.dir_text = dir_text
        self.dir_fullname = dir_fullname
        if not playlists:
            self.is_radio = False
        else:
            self.is_radio = True
            # save radio Playlist texts in dict

    def get_radio_name(self,  playlist_nr):
        return ""

if __name__ == "__main__":
    directories = SimplDirectories(['01-Test',  '02-Peter und der Wolf', '04-Die_Prinzessin','lala'])
    print(directories.get_text_for_folder(2))
    print(directories.get_folder_uri_for_mpd(4))
