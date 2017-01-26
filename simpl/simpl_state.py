#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:42:12 2017

@author: mb
"""
import logging

import text_to_speech
import music_player

class SimplState(object):
   call = 0 # shared state variable
   music_player = music_player.MusicPlayer()
   
   def __init__(self):
       self._logger = logging.getLogger(__name__)
       self._speaker = text_to_speech.TextToSpeech() 
   
   def nextState(self,cls):
      self._logger.debug('-> %s' % (cls.__name__,),)
      self.__class__ = cls

   def showState(self):
       self._logger.debug('%s' % (self.__class__.__name__),)
     
   def cbButtonRiseVolume(self):
       self._logger.debug('Button rise Volume pressed')
       self._speaker.say("Lauter")
        
   def cbButtonLowerVolume(self):
       self._logger.debug('Button lower Volume pressed')
       self._speaker.say("Leiser")
        
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
     
class StatePlayer(SimplState):
   def cbButtonStop(self):
       super(StatePlayer, self).cbButtonStop()
       self.music_player.pause()
       self.nextState(StatePaused)
       
   def cbButtonNext(self):
       super(StatePlayer, self).cbButtonNext()
       self.music_player.playNext()
                    
   def cbButtonPrevious(self):
       super(StatePlayer, self).cbButtonPrevious()
       self.music_player.playPrevious()
       
   def cbButtonNumber(self, number):
       super(StatePlayer, self).cbButtonNumber(number)
       self._speaker.say(str(number))
       self.music_player.switchToFolder('01-Test')
          
class StatePaused(StatePlayer):
   def cbButtonStop(self):
       super(StatePaused.__bases__[0], self).cbButtonStop()
       
   def cbButtonPlay(self):
       super(StatePaused, self).cbButtonPlay()
       self.music_player.pause()
       self.nextState(StatePlayer)
