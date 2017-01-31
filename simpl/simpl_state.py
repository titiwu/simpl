#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:42:12 2017

@author: mb
"""
import logging

import text_to_speech
import music_player
import music_directories

class SimplState(object):
    
    _act_folder_nr = 0
    _act_sond_nr = 0

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._speaker = text_to_speech.TextToSpeech() 
        self._music_player = music_player.MusicPlayer()
        self._directories = music_directories.SimplDirectories(self._music_player.get_directories())
   
    def nextState(self,cls):
        self._logger.debug('-> %s' % (cls.__name__,),)
        self.__class__ = cls

    def showState(self):
        self._logger.debug('%s' % (self.__class__.__name__),)

    def cbButtonRiseVolume(self):
       self._logger.debug('Button rise Volume pressed')
       self.say("Lauter")
        
    def cbButtonLowerVolume(self):
       self._logger.debug('Button lower Volume pressed')
       self.say("Leiser")
        
    def cbButtonPlay(self):
        self._logger.debug('Play button pressed')
  
    def cbButtonStop(self):
        self._logger.debug('Stop button pressed')
 
    def cbButtonNext(self):
        self._logger.debug('Next button pressed')

    def cbButtonPrevious(self):
        self._logger.debug('Last button pressed')

    def cbButtonNumber(self, number):
       self._logger.debug('Button playlist number '+str(number)+' pressed')
       
    def say(self,  full_text):
        """ Wrapper for Text to speech class."""
        self._music_player.pause()
        self._speaker.say(full_text)
        self._music_player.pause()
     
class StatePlayer(SimplState):
    def cbButtonStop(self):
        super(StatePlayer, self).cbButtonStop()
        self._music_player.pause()
        self.nextState(StatePaused)

    def cbButtonNext(self):
        super(StatePlayer, self).cbButtonNext()
        self._music_player.play_next()
 
    def cbButtonPrevious(self):
        super(StatePlayer, self).cbButtonPrevious()
        self._music_player.play_previous()

    def cbButtonNumber(self, number):
        super(StatePlayer, self).cbButtonNumber(number)
        if not self._directories.folder_exists(number):
            self.say("Keine Musik hinterlegt")
        elif (number == self._act_folder_nr):
            #self.say("Spielt schon")
            pass
        else:
            self._music_player.clear_playlist()
            self.say(self._directories.get_text_for_folder(number))
            self._music_player.switch_to_folder(self._directories.get_folder_uri_for_mpd(number))
            self._music_player.play()
            self._act_folder_nr = number

class StatePaused(StatePlayer):
    def cbButtonStop(self):
        super(StatePaused.__bases__[0], self).cbButtonStop()
       
    def cbButtonPlay(self):
        super(StatePaused, self).cbButtonPlay()
        self._music_player.pause()
        self.nextState(StatePlayer)
