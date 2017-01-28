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
    _texts = dict()
    
    def __init__(self,  directory_names):
        self._logger = logging.getLogger(__name__)
        pattern = re.compile("^([0-9]+)-(.*)")
        for dir_name in directory_names:
            if pattern.fullmatch(dir_name):
                search = pattern.search(dir_name)
                dir_number = int(search.group(1))
                dir_text = search.group(2)
                dir_text = dir_text.replace("-", " ")
                dir_text = dir_text.replace("_", " ")
                dir_text = dir_text.strip()
                self._texts[dir_number] = dir_name
                self._directories[dir_number] = dir_text
        self._logger.info(str(len(self._directories)) +'simpl directories found')

    def get_text_for_folder(self,  folder_number):
        if  folder_number in self._texts:
            return(self._texts[folder_number])
        else:
            return ''

    def get_folder_uri_for_mpd(self, folder_number):
        if  folder_number in self._directories:
            return(self._directories[folder_number])
        else:
            return ''

if __name__ == "__main__":
    directories = SimplDirectories(['01-Test',  '02-Peter und der Wolf', '04-Die_Prinzessin','lala'])
