import logging
from typing import Callable


def error_handler(fn: Callable):
    """
    Guard hook error processing data
    Don't guard stream as it swallow error from chunk
    """
    try:
        return fn()
    except Exception as e:
        print("****************")
        print(e)
        logging.error(e)
