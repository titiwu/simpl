# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:42:50 2017

@author: mb
"""
import logging
import time
import sys
import RPi.GPIO as GPIO

class BridgeToGpio(object):
    """
    Use a button matrix
    GPIO IN 
           12  16  20  21
             |     |      |    |
     6   - 1    2     3    4
     13 - 5    6     7    8
     19 - 9   10   11  12
     26 - 13 14   15  16
     GPIO
     OUT
    """
    COL__INPUT_BMC_NR = (12, 16, 20, 21)
    ROW__OUTPUT_BMC_NR = (6, 13, 19, 26)
    
    def __init__(self, simpl_statemachine):
        self._logger = logging.getLogger(__name__)
        # use Broadcom pin numbering convention
        GPIO.setmode(GPIO.BCM)
        # Set up the GPIO channels - one input and one output
        GPIO.setup(self.COL__INPUT_BMC_NR, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.ROW_OUTPUT_BMC_NR, GPIO.OUT)
        # Setting the output
        GPIO.output(self.ROW_OUTPUT_BMC_NR, GPIO.LOW)
        # Adding events
        GPIO.add_event_detect(self.COL_INPUT_BMC_NR, GPIO.FALLING, callback=self.button_in_col_pressed,  bouncetime=200)
        self._logger.debug('GPIO setup done')

    def button_in_col_pressed(self,  channel):
        ''' Set rows high one by one to see when the input disapears '''
        self._logger.debug('Event on input'+str(channel))
        for row_nr in range(0, len(self.ROW_OUTPUT_BMC_NR)-1):
            GPIO.output(self.ROW_OUTPUT_BMC_NR[row_nr], GPIO.HIGH)
            time.sleep(0.02)
            if GPIO.input(channel):
                col = self.COL__INPUT_BMC_NR.index(channel)
                button_nr = row_nr * len(self.COL__INPUT_BMC_NR) + col +1
                self._logger.debug('Button Nr is'+str(button_nr))
                break
        GPIO.output(self.ROW_OUTPUT_BMC_NR, GPIO.LOW)
        #TODO Setters for callback functions for each button number
        
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
    
    SimplGpio = BridgeToGpio()
    try:
        while(True):
            time.sleep(1);
    except KeyboardInterrupt:
        SimplGpio.delete()       # clean up GPIO on CTRL+C exit
