# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:43:33 2017

@author: mb
"""
# respond to a key without the need to press enter

import tkinter as tk
import logging
import queue
from . import simpl


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
        button = self.mapping_to_buttons(event)
        if button:
            self._event_queue.put_nowait(button)
        else:
            self._logger.warning('Mapping to button failed for {}'.format(event.char))

    @staticmethod
    def mapping_to_buttons(key_event) -> simpl.Buttons:
        x = key_event.char
        if x.isdigit():
            simpl.Buttons(int(x))
        elif x == 'p':
            return simpl.Buttons.Play
        elif x == 's':
            return simpl.Buttons.Stop
        elif key_event.keysym == 'Left':
            return simpl.Buttons.Previous
        elif key_event.keysym == 'Right':
            return simpl.Buttons.Next
        elif key_event.keysym == 'Up':
            return simpl.Buttons.VolumeUp
        elif key_event.keysym == 'Down':
            return simpl.Buttons.VolumeDown
        else:
            return None
