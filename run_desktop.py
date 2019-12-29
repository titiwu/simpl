# -*- coding: utf-8 -*-
"""
This is a test file
"""

import logging
from simpl import simpl
from simpl import bridge_to_keyboard

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s]: %(name)s - %(message)s')
logger = logging.getLogger(__name__)


logger.info("Setup simple")
simpl_main = simpl.EventWorker()
logger.info("Setup keyboard watcher")
simpl_main.start()
keyboard_watcher = bridge_to_keyboard.BridgeToKeyboard(simpl_main.event_queue)

