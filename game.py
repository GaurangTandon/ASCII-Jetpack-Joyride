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
from obstacle import FireBeam, Magnet


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
        rowRange = list(map(round, info["rows"]))
        colRange = list(map(round, info["cols"]))
        code = info["objCode"]

        self.grid[rowRange[0]:rowRange[1] + 1,
                  colRange[0]:colRange[1] + 1] = code

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

        self.randomSpawningObjects = [FireBeam, Magnet, CoinGroup]

        self.gameLength = 120
        self.endTime = time.time() + self.gameLength

        self.KEYS = NonBlockingInput()
        clearTerminalScreen()
        self.KEYS.nb_term()

        self.loop()

    def getTimeRemaining(self):
        timeRemaining = (self.endTime - time.time())
        return int(np.round(timeRemaining))

    def infoPrint(self):
        print(f"Time remaining \u23f1 {self.getTimeRemaining()} seconds")
        print(f"Lives remaining \u2764 {self.player.lifes}")
        print("Score", self.score)

    def draw(self):
        # can we fix this to only repaint pixels that changed
        self.grid = np.array([[GRID_CONSTS["background"]
                               for _ in range(self.X)] for _ in range(self.Y)])

        self.infoPrint()

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

    def update(self):
        for obj in self.renderedObjects:
            obj.update()

        for randomSpawn in self.randomSpawningObjects:
            if random.random() < randomSpawn.spawnProbability:
                self.renderedObjects.append(randomSpawn())

        self.player.checkBounds()

    """
    user wants to terminate the game
    """

    def terminate(self):
        self.GAME_STATUS = -1
        print("\nGame over!")
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

            if self.player.lifes == 0 or self.getTimeRemaining() <= 0:
                self.terminate()

            while time.time() - last < self._refresh_time:
                pass
