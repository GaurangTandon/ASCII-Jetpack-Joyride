from threading import Timer
from colorama import init as coloramaInit, Fore, Back, Style
import signal
from player import Player
from util import clearTerminalScreen, GRID_CONSTS


class Game():
    FRAME_RATE = 1
    _refresh_time = 1 / FRAME_RATE
    COLOR_MAP = {
        "player": ["red", None],
        "background": [None, "blue"],
        "ground": [None, "green"]
    }

    SYMBOL_MAP = {
        "player": "p",
        "background": " ",
        "ground": " "
    }

    def initGridConsts(self):
        self.SYMBOL_COLOR_MAP = {}
        assert(self.COLOR_MAP.keys() == GRID_CONSTS.keys())
        for symbol, color in self.COLOR_MAP.items():
            self.SYMBOL_COLOR_MAP[GRID_CONSTS[symbol]] = color

        self.SYMBOL_PAINT_MAP = {}
        for symbol, paint in self.SYMBOL_MAP.items():
            self.SYMBOL_PAINT_MAP[GRID_CONSTS[symbol]] = paint

    def __init__(self):
        coloramaInit()

        self.initGridConsts()

        # TODO: should be based on terminal height
        self.X = 100
        self.Y = 50
        self.player = Player()
        self.loop()
        # doens't work!@!:@#Q@#
        # Timer(self._refresh_time, self.loop)

    def draw(self):
        grid = [[GRID_CONSTS["background"]
                 for _ in range(self.Y)] for _ in range(self.X)]
        self.player.draw(grid)

        for row in grid:
            s = ""
            for cell in row:
                color = self.SYMBOL_COLOR_MAP[cell]
                sym = self.SYMBOL_PAINT_MAP[cell]
                s += Style.RESET_ALL

                if color[0]:
                    s += Fore.RED

                if color[1]:
                    s += Back.BLUE

                s += sym

            print(f"{s}")

    def loop(self):
        clearTerminalScreen()
        self.draw()
        # signal.signal(signal.SIGALRM, self.loop)
        # signal.setitimer(signal.ITIMER_REAL, self._refresh_time)
