import sys
import logging

from . import simpl_state
from . import bridge_to_keyboard


def main(args=None):
    """The main routine."""
    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
                                  "%H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    simple_statemachine = simpl_state.StatePlaying()
    bridge_to_keyboard.BridgeToKeyboard(simple_statemachine)


if __name__ == "__main__":
    main()
