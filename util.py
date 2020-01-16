"""
Utility functions:
    - clear screen
    - take non-blocking keyinput
    - timer settimeout
"""

import subprocess as sp
import threading
from functools import wraps


def clear_terminal_screen():
    """
    Clears terminal screen
    """
    sp.call('clear', shell=True)


def reposition_cursor():
    """
    Reposition cursor to top left of screen
    """
    print("\033[0;0H")


def tiler(elm, row, col, send_matrix=False):
    """
    creates a new matrix of (row, col) shape with every element = elm
    """
    res = []

    for _ in range(row):
        res2 = []
        for __ in range(col):
            res2.append(elm)
        res.append(res2)

    return res[0] if row == 1 and not send_matrix else res


def get_key_pressed(keyin):
    keyin = keyin.lower()

    if not keyin in ('q', ' ', 'w', 'a', 's', 'd', '1', '2', '3', '4'):
        return 0
    if keyin == 'q':
        return -1

    return keyin
