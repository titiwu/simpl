# -*- coding: utf-8 -*-
"""
This is a test file
"""

import logging

import os
import sys

lib_path = os.path.abspath('./simpl')
sys.path.insert(0,lib_path)

import simpl_state
import bridge_to_keyboard


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s",
                                    "%H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

simple_statemachine = simpl_state.StatePlayer()
keyboard_watcher = bridge_to_keyboard.BridgeToKeyboard(simple_statemachine)

