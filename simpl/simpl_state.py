#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:42:12 2017

@author: mb
"""
import logging

from. import text_to_speech
from. import music_player
from. import music_directories


class SimplState(object):
    """Base  State for simpl music player

    Attributes:
        _act_folder_nr: Actual playing folder
        _act_song_nr: Actual playing song
    """
    _act_folder_nr = 0
    _act_song_nr = 0
    _act_vol = 50
    _is_playing = False
    MAXIMUM_VOLUME = 100
    MINIMUM_VOLUME = 10

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._speaker = text_to_speech.TextToSpeech()
        self._music_player = music_player.MusicPlayer()
        self._directories = music_directories.SimplDirectories(self._music_player.get_directories())
        # Init volume
        self._music_player.set_volume(self._act_vol)
        self.say('Simpl Mjusik Pläia ist bereit')

    def nextState(self, cls):
        """Switching to next state"""
        self._logger.debug('-> %s' % (cls.__name__,), )
        self.__class__ = cls

    def showState(self):
        """Print actual state"""
        self._logger.debug('%s' % (self.__class__.__name__), )

    def cbButtonRiseVolume(self):
        """Rise playback volume"""
        self._logger.debug('Button rise Volume pressed')
        self._act_vol = self._act_vol + 10
        if self._act_vol > self.MAXIMUM_VOLUME:
            self._act_vol = self.MAXIMUM_VOLUME
            self.say("Lauter geht nicht")
        self._music_player.set_volume(self._act_vol)

    def cbButtonLowerVolume(self):
        """Lower playback volume"""
        self._logger.debug('Button lower Volume pressed')
        self._act_vol = self._act_vol - 10
        if self._act_vol < self.MINIMUM_VOLUME:
            self._act_vol = self.MINIMUM_VOLUME
            self.say("Leiser geht nicht")
        self._music_player.set_volume(self._act_vol)

    def cbButtonPlay(self):
        self._logger.debug('Play button pressed')

    def cbButtonStop(self):
        self._logger.debug('Stop button pressed')

    def cbButtonNext(self):
        self._logger.debug('Next button pressed')

    def cbButtonPrevious(self):
        self._logger.debug('Last button pressed')

    def cbButtonNumber(self, number):
        self._logger.debug('Button playlist number ' + str(number) + ' pressed')

    def say(self, full_text):
        """ Wrapper for Text to speech class."""
        self._music_player.pause()
        self._speaker.say(full_text)
        self._music_player.pause()


class StatePlaying(SimplState):
    def cbButtonPlay(self):
        super(StatePlaying, self).cbButtonPlay()
        if not self._is_playing:
            self._music_player.pause()
            self._is_playing = True

    def cbButtonStop(self):
        super(StatePlaying, self).cbButtonStop()
        if self._is_playing:
            self._music_player.pause()
            self._is_playing = False

    def cbButtonNext(self):
        super(StatePlaying, self).cbButtonNext()
        # Say next song nr
        max_nr = self._directories.get_nr_of_folder_entries(self._act_folder_nr)
        act_nr = self._music_player.get_act_song_nr()
        next_song_nr = (act_nr + 1) % (max_nr + 1)
        self.say(str(next_song_nr))
        self._music_player.play_next()

    def cbButtonPrevious(self):
        super(StatePlaying, self).cbButtonPrevious()
        # Say previous song nr
        max_nr = self._directories.get_nr_of_folder_entries(self._act_folder_nr)
        act_nr = self._music_player.get_act_song_nr()
        previous_song_nr = (act_nr - 1) % (max_nr + 1)
        self.say(str(previous_song_nr))
        self._music_player.play_previous()

    def cbButtonNumber(self, number):
        super(StatePlaying, self).cbButtonNumber(number)
        if not self._directories.folder_exists(number):
            self.say("Keine Musik hinterlegt")
        elif (number == self._act_folder_nr):
            # self.say("Spielt schon")
            pass
        else:
            self._act_folder_nr = number
            self._act_song_nr = 0
            self.say(self._directories.get_text_for_folder(self._act_folder_nr))
            if self._directories.is_radio_folder(self._act_folder_nr):
                self.say(self._directories.get_radio_playlist_text(self._act_folder_nr, self._act_song_nr))
                self._music_player.switch_to_playlist(
                    self._directories.get_radio_uri_for_mpd(self._act_folder_nr, self._act_song_nr))
                self.nextState(StatePlayingRadio)
            else:
                self._music_player.switch_to_folder(self._directories.get_folder_uri_for_mpd(self._act_folder_nr))
                self.nextState(StatePlaying)
            self._music_player.play()


class StatePlayingRadio(StatePlaying):
    """A radio playlist is being played"""

    def cbButtonNext(self):
        super((self.__class__.__bases__)[0], self).cbButtonNext()
        self._act_song_nr = self._directories.get_next_radio_playlist_nr(self._act_folder_nr, self._act_song_nr)
        self.say(self._directories.get_radio_playlist_text(self._act_folder_nr, self._act_song_nr))
        self._music_player.switch_to_playlist(
            self._directories.get_radio_uri_for_mpd(self._act_folder_nr, self._act_song_nr))

    def cbButtonPrevious(self):
        super((self.__class__.__bases__)[0], self).cbButtonPrevious()
        self._act_song_nr = self._directories.get_previous_radio_playlist_nr(self._act_folder_nr, self._act_song_nr)
        self.say(self._directories.get_radio_playlist_text(self._act_folder_nr, self._act_song_nr))
        self._music_player.switch_to_playlist(
            self._directories.get_radio_uri_for_mpd(self._act_folder_nr, self._act_song_nr))
