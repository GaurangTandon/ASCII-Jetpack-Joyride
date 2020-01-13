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

    if not keyin in ('q', ' ', 'w', 'a', 'd', '1', '2', '3', '4'):
        return 0
    if keyin == 'q':
        return -1

    return keyin


class NonBlockingInput():
    def __init__(self):
        """
        Initializes the object to be used for non-blocking input.
         - Saves original state at time of function call
         - Conversion to new mode has to be manual
        """
        self.old_settings = termios.tcgetattr(sys.stdin)

    @classmethod
    def nb_term(cls):
        """
        Sets up the terminal for non-blocking input
        """
        tty.setcbreak(sys.stdin.fileno())

    def or_term(self):
        """
        Sets terminal back to original state
        """
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_settings)

    @classmethod
    def kb_hit(cls):
        """
        returns True if keypress has occured
        """
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    @classmethod
    def get_ch(cls):
        """
        returns input character
        """
        return sys.stdin.read(1)

    @classmethod
    def flush(cls):
        """
        clears input buffer
        """
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
