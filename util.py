"""
Utility functions:
    - clear screen
    - take non-blocking keyinput
    - timer settimeout
"""

import sys
import select
import tty
import termios
import subprocess as sp
import threading
from functools import wraps


def clear_terminal_screen():
    sp.call('clear', shell=True)


def reposition_cursor():
    print("\033[0;0H")


def tiler(elm, row, col):
    res = []

    for r in range(row):
        res2 = []
        for c in range(col):
            res2.append(elm)
        res.append(res2)

    return res[0] if row == 1 else res


def delay(delay_time=0.):
    """
    Decorator delaying the execution of a function for a while.
    """
    def wrap(function):
        @wraps(function)
        def delayed(*args, **kwargs):
            timer = threading.Timer(
                delay_time, function, args=args, kwargs=kwargs)
            timer.start()
        return delayed
    return wrap


class Timer():
    to_clear_timer = False

    def set_timeout(self, function, time):
        is_invocation_cancelled = False
        @delay(time)
        def some_fn():
            if self.to_clear_timer is False:
                function()
            else:
                print('Invokation is cleared!')
        some_fn()
        return is_invocation_cancelled

    def set_clear_timer(self):
        self.to_clear_timer = True


def get_key_pressed(keyin):
    keyin = keyin.lower()

    if not keyin in ('q', ' ', 'w', 'a', 's', 'd', '1', '2', '3', '4'):
        return 0
    if keyin == 'q':
        return -1

    return keyin
