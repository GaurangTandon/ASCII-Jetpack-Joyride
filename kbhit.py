#!/usr/bin/env python
'''
A Python class implementing KBHIT, the standard keyboard-interrupt poller.
Works transparently on Windows and Posix (Linux, Mac OS X).  Doesn't work
with IDLE.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

'''


import sys
import termios
import atexit
from select import select


class KBHit:
    """
    To take input
    """

    def __init__(self):
        '''Creates a KBHit object that you can call to do various keyboard things.
        '''

        # Save the terminal settings
        self.__fdd = sys.stdin.fileno()
        self.__new_term = termios.tcgetattr(self.__fdd)
        self.__old_term = termios.tcgetattr(self.__fdd)

        # New terminal setting unbuffered
        self.__new_term[3] = (self.__new_term[3] & ~
                              termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.__fdd, termios.TCSAFLUSH, self.__new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        ''' Resets to normal terminal
        '''

        termios.tcsetattr(self.__fdd, termios.TCSAFLUSH, self.__old_term)

    @staticmethod
    def getch():
        ''' Returns a keyboard character after kbhit() has been called.
        '''

        reader = sys.stdin.read(1)
        # sys.stdin.flush()
        return reader

    @staticmethod
    def kbhit():
        ''' Returns True if keyboard character was hit, False otherwise.
        '''
        drr, _, _ = select([sys.stdin], [], [], 0)
        return drr != []
