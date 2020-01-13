import random
import time
import numpy as np
from colorama import init as coloramaInit, Fore, Back, Style
from player import Player
from kbhit import KBHit
from util import clear_terminal_screen, get_key_pressed, reposition_cursor
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

    SYMBOL_COLOR_MAP = {}
    SYMBOL_PAINT_MAP = {}

    def init_grid_consts(self):
        assert self.COLOR_MAP.keys() == GRID_CONSTS.keys()
        for symbol, color in self.COLOR_MAP.items():
            self.SYMBOL_COLOR_MAP[GRID_CONSTS[symbol]] = color

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

        self.game_status = 0

        self.player = Player(self)
        self.ground = Ground()
        self.rendered_objects.append(self.player)
        self.rendered_objects.append(self.ground)

        self.game_length = 120
        self.end_time = time.time() + self.game_length

        self.next_spawn_point = 0

        self.has_boss_spawned = False
        self.magnet_obj = None

        self.keys = KBHit()
        clear_terminal_screen()

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
                               for _ in range(config.FRAME_WIDTH)]
                              for _ in range(config.FRAME_HEIGHT)])

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
        i = -1
        list_of_idxs_to_delete = []

        for obj in self.rendered_objects:
            i += 1
            if obj == self.player:
                continue
            if obj.update() == GenericFrameObject.DEAD_FLAG:
                list_of_idxs_to_delete.append(i)

        list_of_idxs_to_delete.reverse()

        for i in list_of_idxs_to_delete:
            if self.rendered_objects[i].cleanup():
                self.magnet_obj = None
            self.rendered_objects.pop(i)

        # make spawning random somehow
        # make two slots in y axis as well
        if not config.DEBUG:
            if self.player.x + config.FRAME_WIDTH > self.next_spawn_point:
                for random_spawn in [FireBeam, CoinGroup]:
                    threshold = random_spawn.spawn_probability()

                    if random.random() < threshold:
                        obj = random_spawn()
                        self.rendered_objects.append(obj)
                        self.next_spawn_point = max(
                            self.next_spawn_point, obj.x + obj.width)
                        break

            # there should be no magnet if there is a boss
            # since otherwise it is almost impossible to win
            # TODO: see if necessary
            if not self.magnet_obj and not self.has_boss_spawned:
                if random.random() < Magnet.SPAWN_PROBABILITY:
                    self.magnet_obj = Magnet()
                    self.rendered_objects.append(self.magnet_obj)

    def terminate(self):
        """
        user wants to terminate the game
        """
        self.game_status = -1
        print("\nGame over!")
        self.info_print()

    def handle_input(self):
        inputted = ""

        if self.keys.kbhit():
            inputted = self.keys.getch()

        cin = get_key_pressed(inputted)

        if cin == -1:
            self.terminate()
        elif cin != 0:
            if cin in '1234' and config.DEBUG:
                if cin == '1':
                    self.rendered_objects.append(CoinGroup())
                if cin == '2':
                    self.magnet_obj = Magnet()
                    self.rendered_objects.append(self.magnet_obj)
                if cin == '3':
                    self.rendered_objects.append(FireBeam())

            if cin == ' ':
                self.rendered_objects.append(self.player.fire_laser())

        return cin

    def loop(self):
        self.game_status = 1

        last_key_pressed = ""
        clear_terminal_screen()

        while self.game_status == 1:
            # switch to non terminal clearing later
            reposition_cursor()
            # clear_terminal_screen()

            debugStr = f"[{self.player.x} {self.player.y}] \
[{self.player.x_vel} {self.player.y_vel}] \
[{self.player.x_acc} {self.player.y_acc}]" + " " * 50
            # if config.DEBUG:
            #     with open("log", "a") as f:
            #         f.write(debugStr)

            if config.DEBUG:
                print(debugStr)

            self.draw()
            self.update()
            self.player.update(last_key_pressed)

            if not self.has_boss_spawned and self.player.x >= Boss.X_THRESHOLD:
                self.has_boss_spawned = True
                self.rendered_objects.append(Boss(self))
                # TODO: see other comment
                if self.magnet_obj:
                    self.magnet_obj.destroy()

            last = time.time()
            last_key_pressed = self.handle_input()

            if self.player.lifes == 0 or self.get_time_remaining() <= 0:
                self.terminate()

            while time.time() - last < self._refresh_time:
                pass
