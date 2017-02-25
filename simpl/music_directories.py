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
    
    def __init__(self,  directory_list):
        self._logger = logging.getLogger(__name__)
        self.process_directories(directory_list)
        
    def folder_exists(self,  folder_number):
        if  folder_number in self._directories:
            return True
        else:
            return False

    def get_text_for_folder(self,  folder_number):
        if  self.folder_exists(folder_number):
            return(self._directories[folder_number].dir_text)
        else:
            return 'Nichts hinterlegt'

    def get_folder_uri_for_mpd(self, folder_number):
        if  self.folder_exists(folder_number):
            return(self._directories[folder_number].dir_fullname)
        else:
            return ''
    def get_nr_of_folder_entries(self,  folder_number):
        if  self.folder_exists(folder_number):
            return(self._directories[folder_number].nr_of_entries)
        else:
            return 0

    def is_radio_folder(self, folder_number):
        """Returns if a given folder contains radio playlists"""
        if  self.folder_exists(folder_number):
            return(self._directories[folder_number].is_radio)
        else:
            return False

    def get_radio_playlist_text(self, folder_number,  playlist_nr):
        """Returns text for the radio playlist (e.g. radio station)"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_radio_name(playlist_nr)
        else:
            return 'Fehler'

    def get_radio_uri_for_mpd(self, folder_number,  playlist_nr):
        """Returns the URI needed to add the radio-playlist to the mpd playlist"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_full_radio_uri(playlist_nr)
        else:
            return ''

    def get_next_radio_playlist_nr(self,  folder_number,  playlist_nr):
        """Get next playlist"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_next_playlist_number(playlist_nr)
        else:
            return 0
            
    def get_previous_radio_playlist_nr(self,  folder_number,  playlist_nr):
        """Get previous playlist"""
        if self.is_radio_folder(folder_number):
            return self._directories[folder_number].get_previous_playlist_number(playlist_nr)
        else:
            return 0

    def process_directories(self,  directory_list):
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
                self._directories[dir_number] = MusicFolder(dir_text,  dir_name,  directory['files'],  directory['playlists'])
        self._logger.info(str(len(self._directories)) +'simpl directories found')

class MusicFolder(object):
    """Music folder properties."""
    is_radio = False
    dir_text = ""
    dir_fullname = ""
    nr_of_entries = 0
    radio_playlists = list()
    
    def __init__(self,  dir_text,  dir_fullname,  file_names,  playlists):
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

    def get_full_radio_uri(self,  playlist_nr):
        if playlist_nr < 0 or playlist_nr > len(self.radio_playlists):
            self._logger.info('Playlist nr'+str(playlist_nr)+'not in directory'+self.dir_fullname)
            return ''
        return self.dir_fullname+'/'+self.radio_playlists[playlist_nr]

    def get_radio_name(self,  playlist_nr):
        if playlist_nr < 0 or playlist_nr > len(self.radio_playlists):
            self._logger.info('Playlist nr'+str(playlist_nr)+'not in directory'+self.dir_fullname)
            return "Fehler"
        return self.radio_playlists[playlist_nr].split('.', 1)[0] .replace("_", " ").replace("-", " ")

    def get_next_playlist_number(self,  act_nr):
        """Return next number in playlist, wrapping round"""
        if self.nr_of_entries == 0:
            return 0
        else:
            return (act_nr + 1) % (self.nr_of_entries +1) 

    def get_previous_playlist_number(self,  act_nr):
        """Return previous number in playlist, wrapping round"""
        if self.nr_of_entries == 0:
            return 0
        else:
            return (act_nr - 1) % (self.nr_of_entries +1) 

if __name__ == "__main__":
    dir_list = [{'playlists': [], 
                      'directory': '01-Test', 
                      'files': ['Doobie Brothers - Without Love (Where would you be now).mp3', 'Frank Sinatra - New York New York.mp3', 'Al Jarreau - Boogie Down.wma', 'Curtis Mayfield - Move On Up.mp3', 'Buckshot LeFonque -Some Cow Funk (more tea, vicar).wma', 'Frank Sinatra - You make me feel so young.mp3', 'Frank Sinatra - The Lady is a Tramp.mp3', "Frank Sinatra - I've got you under my Skin.mp3", 'Frank Sinatra - Nice work if you can get it.mp3', 'Earth Wind & Fire - Shinning Star.mp3', 'Earth Wind & Fire - Mix funk.mp3', 'Earth, Wind & Fire - Got To Get You Into My Life.mp3']}, 
                    {'playlists': [], 
                      'directory': '02-Peter und der Wolf', 
                      'files': ['Peter Fox - Die Affen steigen auf den Thron.mp3', 'Peter Fox - Lok auf 2 Beinen.mp3', 'Peter Fox - Der letzte Tag.mp3', 'Peter Fox - Stadtaffe.mp3', 'Peter Fox - Haus am See.mp3', 'Peter Fox - Kopf verloren.mp3', 'Peter Fox - Das zweite Gesicht.mp3', 'Peter Fox - Schwinger.mp3', 'Peter Fox - Ich Steine, Du Steine.mp3', 'Peter Fox - Fieber.mp3', 'Peter Fox - Schuttel deinen Speck.mp3', 'Peter Fox - Grosshirn RMX.mp3', 'Peter Fox - Schwarz zu Blau.mp3', 'Peter Fox - She moved in (Miss Platnum).mp3', 'Peter Fox - Marry me (feat. Miss Platnum).mp3', 'Peter Fox - Aufstehn.mp3', 'Peter Fox - Alles Neu.mp3', 'Peter Fox - Dickes Ende.mp3']}, 
                    {'playlists': [], 
                      'directory': '03-Die_Prinzessin', 
                      'files': ['01 dota_kehr - zeitgeist.mp3', '02 dota_kehr - sternschnuppen.mp3', '03 dota_kehr - zauberer.mp3', '04 dota_kehr - selten_aber_manchmal.mp3', '05 dota_kehr - friedberg.mp3', '06 dota_kehr - mediomelo.mp3', '07 dota_kehr - kaulquappe.mp3', '08 dota_kehr - schneeknig.mp3', '09 dota_kehr - nichts_neues.mp3', '10 dota_kehr - geheimnis.mp3', '11 dota_kehr - erledigungszettelschreiber.mp3', '12 dota_kehr - die_drei.mp3']}, 
                    {'playlists': ['bayern_2.m3u', 'M_94_5.ogg.m3u', 'F_M_4.pls'], 
                      'directory': '04-Radio', 
                      'files': []}]
    
    directories = SimplDirectories(dir_list)
    print(directories.get_text_for_folder(2))
    print(directories.get_folder_uri_for_mpd(4))
    print(directories._directories[1].get_radio_name(2))
    print(directories._directories[4].get_radio_name(2))
    print(directories.get_radio_uri_for_mpd(4, 0))
