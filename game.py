import random
import time
import numpy as np
from colorama import init as coloramaInit, Fore, Back, Style
from player import Player
from util import clear_terminal_screen, NonBlockingInput, get_key_pressed
import config
from config import GRID_CONSTS, FRAME_RATE
from ground import Ground
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

    def init_grid_consts(self):
        self.SYMBOL_COLOR_MAP = {}
        assert self.COLOR_MAP.keys() == GRID_CONSTS.keys()
        for symbol, color in self.COLOR_MAP.items():
            self.SYMBOL_COLOR_MAP[GRID_CONSTS[symbol]] = color

        self.SYMBOL_PAINT_MAP = {}
        for symbol, paint in self.SYMBOL_MAP.items():
            self.SYMBOL_PAINT_MAP[GRID_CONSTS[symbol]] = paint

    # info bounding indices are inclusive
    def draw_in_range(self, info, obj):
        to_row = round(info["coord"][0])
        from_row = to_row - info["size"][0] + 1

        from_col = round(info["coord"][1])
        to_col = from_col + info["size"][1] - 1

        # print(info, obj)
        self.grid[from_row: to_row + 1,
                  from_col:to_col + 1] = obj

    def __init__(self):
        coloramaInit()

        self.init_grid_consts()
        self.score = 0

        self.grid = [[]]
        self.rendered_objects = []

        self.X = config.FRAME_WIDTH
        self.Y = config.FRAME_HEIGHT
        self.GAME_STATUS = 0

        self.player = Player(self)
        self.ground = Ground()
        self.rendered_objects.append(self.player)
        self.rendered_objects.append(self.ground)

        self.random_spawning_objects = [FireBeam, Magnet, CoinGroup]

        self.game_length = 120
        self.end_time = time.time() + self.game_length

        self.next_spawn_point = 0

        self.has_boss_spawned = False

        self.KEYS = NonBlockingInput()
        clear_terminal_screen()
        self.KEYS.nb_term()

        self.loop()

    def get_time_remaining(self):
        time_remaining = (self.end_time - time.time())
        return int(np.round(time_remaining))

    def info_print(self):
        print(f"Time remaining \u23f1 {self.get_time_remaining()} seconds")
        print(f"Lives remaining \u2764 {self.player.lifes}")
        print(f"Score {self.score}")
        if not self.has_boss_spawned:
            print(
                f"Distance to boss {Boss.X_THRESHOLD - self.player.x}")
        else:
            print("Boss has spawned!")

    def draw(self):
        # TODO: can we fix this to only repaint pixels that changed
        self.grid = np.array([[Fore.WHITE + Back.BLUE + " "
                               for _ in range(self.X)] for _ in range(self.Y)])

        self.info_print()

        for obj in self.rendered_objects:
            info_objs = obj.draw()
            for info in info_objs:
                self.draw_in_range(info, obj.obj)

        print_grid = "\n".join([(Style.RESET_ALL).join(row) + Style.RESET_ALL
                                for row in self.grid])

        # only a single print at the end makes rendering efficient
        print(print_grid)

    def update(self):
        i = 0
        list_of_idxs_to_delete = []

        for obj in self.rendered_objects:
            if obj.update() == GenericFrameObject.DEAD_FLAG:
                list_of_idxs_to_delete.append(i)
            i += 1

        list_of_idxs_to_delete.reverse()

        for i in list_of_idxs_to_delete:
            self.rendered_objects[i].cleanup()
            self.rendered_objects.pop(i)

        # make spawning random somehow
        # make two slots in y axis as well
        if self.player.x + config.FRAME_WIDTH > self.next_spawn_point:
            for random_spawn in self.random_spawning_objects:
                threshold = random_spawn.spawn_probability()

                if random.random() < threshold:
                    obj = random_spawn()
                    self.rendered_objects.append(obj)
                    self.next_spawn_point = max(
                        self.next_spawn_point, obj.x + obj.width)
                    break

        self.player.check_bounds()

        if not self.has_boss_spawned and self.player.x >= Boss.X_THRESHOLD:
            self.has_boss_spawned = True
            self.rendered_objects.append(Boss(self))

    def terminate(self):
        """
        user wants to terminate the game
        """
        self.GAME_STATUS = -1
        print("\nGame over!")
        self.info_print()

    def handle_input(self):
        inputted = ""
        if self.KEYS.kb_hit():
            inputted = self.KEYS.get_ch()

        cin = get_key_pressed(inputted)

        if cin == -1:
            self.terminate()
        elif cin != 0:
            obj = self.player.update_key(cin)
            if obj:
                self.rendered_objects.append(obj)
        else:
            self.player.reset_no_key()

        self.KEYS.flush()

    def loop(self):
        self.GAME_STATUS = 1

        while self.GAME_STATUS == 1:
            clear_terminal_screen()
            self.draw()
            self.update()

            last = time.time()
            self.handle_input()

            if self.player.lifes == 0 or self.get_time_remaining() <= 0:
                self.terminate()

            while time.time() - last < self._refresh_time:
                pass
