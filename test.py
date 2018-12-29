# -*- coding: utf-8 -*-
"""
This is a test file
"""

import logging
import simpl.simpl_state
import simpl.bridge_to_keyboard

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(name)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("Setup state machine")
simple_statemachine = simpl.simpl_state.StatePlaying()
logger.info("Setup Event worker")
event_processor = simpl.bridge_to_keyboard.EventWorker(simple_statemachine)
event_processor.start()
logger.info("Setup keyboard watcher")
keyboard_watcher = simpl.bridge_to_keyboard.BridgeToKeyboard(event_processor.event_queue)

