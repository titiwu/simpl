# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:42:50 2017

@author: mb
"""
from . import simpl

import logging
import time
import sys
import queue

import RPi.GPIO as GPIO


class BridgeToGpio(object):
    """
    Use a button matrix
    GPIO IN 
     |IN >| 23 | 24 | 25 | 16 |
     |----|----|----|----|----|
     | 22 |  1 |  2 |  3 |  4 |
     |  5 |  5 |  6 |  7 |  8 |
     |  6 |  9 | 10 | 11 | 12 |
     | 26 | 13 | 14 | 15 | 16 |
     |OUT^|----|----|----|----|
     GPIO
     OUT
    """
    COL_INPUT_BMC_NR = (23, 24, 25, 16)
    ROW_OUTPUT_BMC_NR = (22, 5, 6, 26)

    BUTTON_NR_TO_SIMPL_BUTTON = {
        1: simpl.Buttons.ButtonOne,
        2: simpl.Buttons.ButtonTwo,
        3: simpl.Buttons.ButtonThree,
        4: simpl.Buttons.VolumeUp,
        5: simpl.Buttons.ButtonFour,
        6: simpl.Buttons.ButtonFive,
        7: simpl.Buttons.ButtonSix,
        8: simpl.Buttons.VolumeDown,
        9: simpl.Buttons.ButtonSeven,
        10: simpl.Buttons.ButtonEight,
        11: simpl.Buttons.ButtonNine,
        12: simpl.Buttons.Mode,
        13: simpl.Buttons.Previous,
        14: simpl.Buttons.Stop,
        15: simpl.Buttons.Play,
        16: simpl.Buttons.Next
    }

    def __init__(self, event_queue: queue.Queue):
        self._logger = logging.getLogger(__name__)
        self.event_queue = event_queue
        # use Broadcom pin numbering convention
        GPIO.setmode(GPIO.BCM)
        # Set up the GPIO channels - one input and one output
        GPIO.setup(self.COL_INPUT_BMC_NR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.ROW_OUTPUT_BMC_NR, GPIO.OUT)
        # Setting the output
        GPIO.output(self.ROW_OUTPUT_BMC_NR, GPIO.LOW)
        # Adding events
        GPIO.add_event_detect(self.COL_INPUT_BMC_NR[0], GPIO.FALLING, callback=self.button_in_col_pressed,
                              bouncetime=300)
        GPIO.add_event_detect(self.COL_INPUT_BMC_NR[1], GPIO.FALLING, callback=self.button_in_col_pressed,
                              bouncetime=300)
        GPIO.add_event_detect(self.COL_INPUT_BMC_NR[2], GPIO.FALLING, callback=self.button_in_col_pressed,
                              bouncetime=300)
        GPIO.add_event_detect(self.COL_INPUT_BMC_NR[3], GPIO.FALLING, callback=self.button_in_col_pressed,
                              bouncetime=300)
        self._logger.debug('GPIO setup done')

    def button_in_col_pressed(self, channel):
        '''Set rows high one by one to see when the input disapears'''
        self._logger.debug('Event on input ' + str(channel))
        for row_nr in range(0, len(self.ROW_OUTPUT_BMC_NR)):
            GPIO.output(self.ROW_OUTPUT_BMC_NR[row_nr], GPIO.HIGH)
            time.sleep(0.02)
            if GPIO.input(channel):
                col = self.COL_INPUT_BMC_NR.index(channel)
                button_nr = row_nr * len(self.COL_INPUT_BMC_NR) + col + 1
                self._logger.debug('Button Nr is ' + str(button_nr))
                self.event_queue.put(self.BUTTON_NR_TO_SIMPL_BUTTON[button_nr])
                break
        GPIO.output(self.ROW_OUTPUT_BMC_NR, GPIO.LOW)
        # TODO Setters for callback functions for each button number

    def delete(self):
        # Clean up GPIO settings
        self._logger.debug('Cleaning up')
        GPIO.cleanup()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s",
                                  "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    test_queue = queue.Queue()

    SimplGpio = BridgeToGpio(test_queue)

    try:
        while (True):
            time.sleep(1)
            with test_queue.mutex:
                test_queue.queue.clear()
    except (KeyboardInterrupt, SystemExit):
        SimplGpio.delete()  # clean up GPIO on CTRL+C exit
