# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:09:25 2017

@author: mb
"""

import logging
import os
import tempfile
import subprocess
import pipes

import diagnose

class TextToSpeech(object):
    """
    Uses the svox-pico-tts speech synthesizer
    Requires pico2wave to be available
    """
    SOUND_PLAYER="aplay" #Play sound with mplayer, mpg123
    LANGUAGE = "de-DE" #language
    
    def __init__(self):
       self._logger = logging.getLogger(__name__)
       diagnose.check_executable('aplay')

    def output_sound(self, pathToFile, device=''):
        cmd = [self.SOUND_PLAYER,  str(pathToFile)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)

    def say(self, fullText):
        self._logger.debug("Saying '%s' with 'svox pico'", fullText)
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            fname = f.name
        cmd = ['pico2wave', '--wave', fname]
        cmd.extend(['-l', self.LANGUAGE])
        cmd.append(fullText)
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)
        #self.output_sound(fname)
        os.remove(fname)
        
    def cancel():
        pass
# TODO
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    speaker = TextToSpeech();
    speaker.say("Meikrofon tscheck eins zwo")
    speaker.say("Test test")
