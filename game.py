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
from generic import GenericFrameObject
from boss import Boss


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
    def drawInRange(self, info, obj):
        to_row = round(info["coord"][0])
        from_row = to_row - info["size"][0] + 1

        from_col = round(info["coord"][1])
        to_col = from_col + info["size"][1] - 1

        # print(info, obj)
        self.grid[from_row: to_row + 1,
                  from_col:to_col + 1] = obj

    def __init__(self):
        coloramaInit()

        self.initGridConsts()
        self.score = 0

        self.renderedObjects = []

        self.X = config.FRAME_WIDTH
        self.Y = config.FRAME_HEIGHT
        self.GAME_STATUS = 0

        self.player = Player(self)
        self.ground = Ground()
        self.renderedObjects.append(self.player)
        self.renderedObjects.append(self.ground)

        self.randomSpawningObjects = [FireBeam, Magnet, CoinGroup]

        self.gameLength = 120
        self.endTime = time.time() + self.gameLength

        self.nextSpawnPoint = 0

        self.hasBossSpawned = False

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
        print(f"Score {self.score}")
        if not self.hasBossSpawned:
            print(
                f"Distance to boss {Boss.X_THRESHOLD - self.player.x}")
        else:
            print("Boss has spawned!")

    def draw(self):
        # TODO: can we fix this to only repaint pixels that changed
        self.grid = np.array([[Fore.WHITE + Back.BLUE + " "
                               for _ in range(self.X)] for _ in range(self.Y)])

        self.infoPrint()

        for obj in self.renderedObjects:
            infoObjs = obj.draw()
            for info in infoObjs:
                self.drawInRange(info, obj.obj)

        printGrid = "\n".join([(Style.RESET_ALL).join(row) + Style.RESET_ALL
                               for row in self.grid])

        # only a single print at the end makes rendering efficient
        print(printGrid)

    def update(self):
        i = 0
        listOfIdxsToDelete = []

        for obj in self.renderedObjects:
            if obj.update() == GenericFrameObject.DEAD_FLAG:
                listOfIdxsToDelete.append(i)
            i += 1

        listOfIdxsToDelete.reverse()

        for i in listOfIdxsToDelete:
            self.renderedObjects[i].cleanup()
            self.renderedObjects.pop(i)

        # make spawning random somehow
        # make two slots in y axis as well
        if self.player.x + config.FRAME_WIDTH > self.nextSpawnPoint:
            for randomSpawn in self.randomSpawningObjects:
                threshold = randomSpawn.spawnProbability()

                if random.random() < threshold:
                    obj = randomSpawn()
                    self.renderedObjects.append(obj)
                    self.nextSpawnPoint = max(
                        self.nextSpawnPoint, obj.x + obj.width)
                    break

        self.player.checkBounds()

        if not self.hasBossSpawned and self.player.x >= Boss.X_THRESHOLD:
            self.hasBossSpawned = True
            self.renderedObjects.append(Boss(self))

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
