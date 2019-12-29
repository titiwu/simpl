from . import simpl_state

import logging
import threading
import queue
import mpd

from enum import Enum


class Buttons(Enum):
    Play = 10
    Stop = 11
    Previous = 12
    Next = 13
    VolumeUp = 14
    VolumeDown = 15
    Mode = 16
    ButtonOne = 1
    ButtonTwo = 2
    ButtonThree = 3
    ButtonFour = 4
    ButtonFive = 5
    ButtonSix = 6
    ButtonSeven = 7
    ButtonEight = 8
    ButtonNine = 9


class EventWorker(threading.Thread):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.event_queue = queue.Queue()
        self._logger.info("Setup state machine")
        self.simple_statemachine = simpl_state.StatePlaying()
        super().__init__()

    def run(self):
        try:
            while True:
                button = self.event_queue.get()
                self.button_pressed(button)
        except KeyboardInterrupt:
            pass

    def button_pressed(self, button: Buttons):
        self._logger.debug("Received {}".format(button))
        try:
            if button.value < 9:
                self.simple_statemachine.cbButtonNumber(button)
            elif button == Buttons.Play:
                self.simple_statemachine.cbButtonPlay()
            elif button == Buttons.Stop:
                self.simple_statemachine.cbButtonStop()
            elif button == Buttons.Previous:
                self.simple_statemachine.cbButtonPrevious()
            elif button == Buttons.Next:
                self.simple_statemachine.cbButtonNext()
            elif button == Buttons.VolumeUp:
                self.simple_statemachine.cbButtonRiseVolume()
            elif button == Buttons.VolumeDown:
                self.simple_statemachine.cbButtonLowerVolume()
            else:
                pass
        except mpd.base.ConnectionError:
            self._logger.info("Lost connection to MPD. Trying to reconnect.")
            self.simple_statemachine.reconnect_mpd()
