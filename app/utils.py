import functools
import logging
import sys
from typing import List

import requests


def logged_method(show_len=False):
    def wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):

            logger_start = logging.getLogger("start")
            logger_len = logging.getLogger("len")

            handler = logging.StreamHandler(stream=sys.stdout)
            handler.setLevel(logging.DEBUG)

            logger_start.addHandler(handler)
            logger_start.setLevel(logging.DEBUG)

            logger_len.addHandler(handler)
            logger_len.setLevel(logging.DEBUG)

            func_name = func.__name__

            logger_start.info("[%s] starting", func_name)

            value = func(*args, **kwargs)
            if show_len:
                logger_len.info("[%s] len: %s", func_name, len(value))
            return value

        return inner_wrapper

    return wrapper


@logged_method(show_len=True)
def get_data_from_url_synchronously(url: str) -> List[dict]:
    try:
        data = requests.get(url).json()
    except requests.ConnectionError as e:
        sys.exit(f"Unable to get data, check Internet connection: \n{e}")
    except Exception as e:
        sys.exit(f"Unable to get data, unknown exception: \n{e}")
    return data
