import sys
import logging

import simpl_state
import bridge_to_keyboard

def main (args=None):
    """The main routine."""
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s",
                                    "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    simple_statemachine = simpl_state.StatePlayer()
    bridge_to_keyboard.BridgeToKeyboard(simple_statemachine)

if __name__ == "__main__":
    main()
