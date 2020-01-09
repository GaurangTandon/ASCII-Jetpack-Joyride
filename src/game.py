from colorama import init as coloramaInit, Fore
import signal
from player import Player
from util import clearTerminalScreen, GRID_CONSTS


class Game():
    FRAME_RATE = 10
    _refresh_time = 1 / FRAME_RATE
    COLOR_MAP = {
        "player": "red",
        "background": "blue",
        "ground": "green"
    }

    SYMBOL_MAP = {
        "player": "p",
        "background": "b",
        "ground": "g"
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
        self.Y = 100
        self.player = Player()
        signal.signal(signal.SIGALRM, self.loop)

        self.loop()

    def draw(self):
        grid = [[GRID_CONSTS["background"]
                 for _ in range(self.Y)] for _ in range(self.X)]
        self.player.draw(grid)

        for row in grid:
            s = ""
            for cell in row:
                color = self.SYMBOL_COLOR_MAP[cell].upper()
                sym = self.SYMBOL_PAINT_MAP[cell]
                s += (Fore.RED + sym)

            print(f"{s}")

    def loop(self):
        clearTerminalScreen()
        self.draw()
        # doesn't loop?
        signal.setitimer(signal.ITIMER_REAL, self._refresh_time)
