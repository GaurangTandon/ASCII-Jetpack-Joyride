import numpy as np
from threading import Timer
from colorama import init as coloramaInit, Fore, Back, Style
import signal
from player import Player
from util import clearTerminalScreen
import config
from config import GRID_CONSTS
from ground import Ground
import time


class Game():
    FRAME_RATE = 1
    _refresh_time = 1 / FRAME_RATE
    COLOR_MAP = {
        "player": [Fore.RED, None],
        "background": [None, Back.BLUE],
        "ground": [None, Back.GREEN],
        "coin": [Fore.YELLOW, None]
    }

    SYMBOL_MAP = {
        "player": "p",
        "background": " ",
        "ground": " ",
        "coin": "C"
    }

    def initGridConsts(self):
        self.SYMBOL_COLOR_MAP = {}
        assert(self.COLOR_MAP.keys() == GRID_CONSTS.keys())
        for symbol, color in self.COLOR_MAP.items():
            self.SYMBOL_COLOR_MAP[GRID_CONSTS[symbol]] = color

        self.SYMBOL_PAINT_MAP = {}
        for symbol, paint in self.SYMBOL_MAP.items():
            self.SYMBOL_PAINT_MAP[GRID_CONSTS[symbol]] = paint

    # info bounding indices are inclusive
    def drawInRange(self, info):
        self.grid[info["from_row"]:info["to_row"] + 1,
                  info["from_col"]:info["to_col"] + 1] = info["objCode"]

    def __init__(self):
        coloramaInit()

        self.initGridConsts()

        # "TODO":should be based on terminal height
        self.X = config.FRAME_WIDTH
        self.Y = config.FRAME_HEIGHT
        self.player = Player()
        self.ground = Ground()
        self.loop()
        # doens't work!@!:@#Q@#
        # Timer(self._refresh_time, self.loop)

    def draw(self):
        self.grid = np.array([[GRID_CONSTS["background"]
                               for _ in range(self.X)] for _ in range(self.Y)])
        self.drawInRange(self.player.draw())
        self.drawInRange(self.ground.draw())

        for row in self.grid:
            for cell in row:
                color = self.SYMBOL_COLOR_MAP[cell]
                sym = self.SYMBOL_PAINT_MAP[cell]
                s = ""

                if color[0]:
                    s += color[0]

                if color[1]:
                    s += color[1]

                s += sym
                print(s + Style.RESET_ALL, end="")

    def loop(self):
        while True:
            clearTerminalScreen()
            self.draw()
            last = time.time()
            while time.time() - last < self._refresh_time:
                pass

        # signal.signal(signal.SIGALRM, self.loop)
        # signal.setitimer(signal.ITIMER_REAL, self._refresh_time)
