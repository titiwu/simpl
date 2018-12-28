# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 21:43:33 2017

@author: mb
"""
# respond to a key without the need to press enter

import tkinter as tk


class BridgeToKeyboard(object):
    def __init__(self, simpl_statemachine):
        self._simpl = simpl_statemachine
        root = tk.Tk()
        root.geometry('300x200')
        self.text = tk.Text(root, background='black', foreground='white', font=('Comic Sans MS', 10))
        self.text.pack()
        root.bind('<KeyPress>', self.onKeyPress)
        root.mainloop()

    def on_key_press(self, event):
        self.text.insert('end', 'You pressed %s\n' % (event.char,))
        x = event.char
        if (x.isdigit()):
            self._simpl.cbButtonNumber(int(x))
        elif (x == 'p'):
            self._simpl.cbButtonPlay()
        elif (x == 's'):
            self._simpl.cbButtonStop()
        elif event.keysym == 'Left':
            self._simpl.cbButtonPrevious()
        elif event.keysym == 'Right':
            self._simpl.cbButtonNext()
        elif event.keysym == 'Up':
            self._simpl.cbButtonRiseVolume()
        elif event.keysym == 'Down':
            self._simpl.cbButtonLowerVolume()
        else:
            pass
