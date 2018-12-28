# -*- coding: utf-8 -*-
"""
This is a test file
"""

import logging
import sys
import simpl.simpl_state
import simpl.bridge_to_keyboard


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s",
                                    "%H:%M:%S")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

simple_statemachine = simpl.simpl_state.StatePlaying()
keyboard_watcher = simpl.bridge_to_keyboard.BridgeToKeyboard(simple_statemachine)

