import numpy as np
from threading import Timer
from colorama import init as coloramaInit, Fore, Back, Style
import signal
from player import Player
from util import clearTerminalScreen, NonBlockingInput, getKeyPressed
import config
from config import GRID_CONSTS, FRAME_RATE
from ground import Ground
import time
import random
from coin import CoinGroup


class Game():
    _refresh_time = 1 / FRAME_RATE
    # TODO: improve rendering with multiple parts of the same object having different colors
    COLOR_MAP = {
        "player": [Fore.RED, None],
        "background": [None, Back.BLUE],
        "ground": [None, Back.GREEN],
        "coin": [Fore.YELLOW, None],
        "firebeam": [Fore.YELLOW, Back.RED],
        "magnet": [Fore.RED, Back.WHITE],
        "playerlaser": [Fore.RED, None]
    }

    SYMBOL_MAP = {
        "player": "p",
        "background": " ",
        "ground": " ",
        "coin": "C",
        "firebeam": "f",
        "magnet": "m",
        "playerlaser": "l"
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
        self.grid[round(info["rows"][0]):round(info["rows"][1] + 1),
                  round(info["cols"][0]):round(info["cols"][1] + 1)] = info["objCode"]

    def __init__(self):
        coloramaInit()

        self.initGridConsts()
        self.score = 0

        self.renderedObjects = []

        self.X = config.FRAME_WIDTH
        self.Y = config.FRAME_HEIGHT
        self.GAME_STATUS = 0

        self.player = Player()
        self.ground = Ground()
        self.renderedObjects.append(self.player)
        self.renderedObjects.append(self.ground)

        self.startTime = time.time()

        self.KEYS = NonBlockingInput()
        clearTerminalScreen()
        self.KEYS.nb_term()

        self.loop()
        # doens't work!@!:@#Q@#3
        # Timer(self._refresh_time, self.loop)

    def infoPrint(self):
        timeSoFar = (time.time() - self.startTime)
        printTime = int(np.round(timeSoFar))
        print(f"Time travelled \u23f1 {printTime} seconds")
        print("Score", self.score)

    def draw(self):
        self.grid = np.array([[GRID_CONSTS["background"]
                               for _ in range(self.X)] for _ in range(self.Y)])

        for obj in self.renderedObjects:
            infoObjs = obj.draw()
            for info in infoObjs:
                self.drawInRange(info)

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
            # this standalone print separates rows
            # and also prevents the render from going haywire, idk how
            print()

        self.infoPrint()

    def update(self):
        for obj in self.renderedObjects:
            obj.update()

        if random.random() < config.COIN_SPAWN_PROBABILITY:
            self.renderedObjects.append(CoinGroup())

    """
    user wants to terminate the game
    """

    def terminate(self):
        self.GAME_STATUS = -1
        print("Game over!")
        self.infoPrint()

    def handleInput(self):
        input = ""
        if self.KEYS.kb_hit():
            input = self.KEYS.get_ch()

        cin = getKeyPressed(input)

        if cin == -1:
            self.terminate()
        elif cin != 0:
            obj = self.player.updateKey(cin)
            if obj:
                self.renderedObjects.append(obj)
        else:
            self.player.resetNoKey()

        self.KEYS.flush()

    def loop(self):
        self.GAME_STATUS = 1

        while self.GAME_STATUS == 1:
            clearTerminalScreen()
            self.draw()
            self.update()

            last = time.time()
            self.handleInput()

            if self.player.lifes == 0:
                self.terminate()

            while time.time() - last < self._refresh_time:
                pass

        # signal.signal(signal.SIGALRM, self.loop)
        # signal.setitimer(signal.ITIMER_REAL, self._refresh_time)
