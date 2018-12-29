# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:43:33 2017

@author: mb
"""
# respond to a key without the need to press enter

import tkinter as tk
import logging
import threading
import queue
import mpd


class BridgeToKeyboard(object):
    def __init__(self, event_queue: queue.Queue):
        self._logger = logging.getLogger(__name__)
        self._event_queue = event_queue
        root = tk.Tk()
        root.geometry('300x200')
        self.text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 10))
        self.text.pack()
        root.bind('<KeyPress>', self.on_key_press)
        root.mainloop()

    def on_key_press(self, event):
        self.text.insert('end', 'You pressed %s\n' % (event.char,))
        self._event_queue.put_nowait(event)


class EventWorker(threading.Thread):
    def __init__(self,  simpl_statemachine):
        self._logger = logging.getLogger(__name__)
        self._simpl = simpl_statemachine
        self.event_queue = queue.Queue()
        super().__init__()

    def run(self):
        try:
            while True:
                key_event = self.event_queue.get()
                self.key_pressed(key_event)
        except KeyboardInterrupt:
            pass

    def key_pressed(self, key_event):
        x = key_event.char
        self._logger.debug("Received "+x)
        try:
            if x.isdigit():
                self._simpl.cbButtonNumber(int(x))
            elif x == 'p':
                self._simpl.cbButtonPlay()
            elif x == 's':
                self._simpl.cbButtonStop()
            elif key_event.keysym == 'Left':
                self._simpl.cbButtonPrevious()
            elif key_event.keysym == 'Right':
                self._simpl.cbButtonNext()
            elif key_event.keysym == 'Up':
                self._simpl.cbButtonRiseVolume()
            elif key_event.keysym == 'Down':
                self._simpl.cbButtonLowerVolume()
            else:
                pass
        except mpd.base.ConnectionError:
            self._logger.info("Lost connection to MPD. Trying to reconnect.")
            self._simpl.reconnect_mpd()


