"""
The actual game and rendering related functions
"""


import os
import random
import math
import time
import numpy as np
from colorama import init as coloramaInit, Fore, Back, Style
from player import Player
from kbhit import KBHit
from util import clear_terminal_screen, get_key_pressed, reposition_cursor
import config
from config import FRAME_RATE
from ground import Ground
from coin import CoinGroup
from obstacle import FireBeam, Magnet
from generic import GenericFrameObject
from boss import Boss
from powerup import DragonPowerup


class Game():
    """
    The actual game and rendering related functions
    """
    _refresh_time = 1 / FRAME_RATE
    GAME_LENGTH = 120

    # info bounding indices are inclusive

    def _draw_in_range(self, info, obj):
        to_row = round(info["coord"][0])
        from_row = to_row - info["size"][0] + 1

        from_col = round(info["coord"][1])
        to_col = from_col + info["size"][1] - 1

        self.grid[from_row: to_row + 1,
                  from_col:to_col + 1] = obj

    def __init__(self):
        coloramaInit()

        self.score = 0

        self.grid = [[]]
        self.rendered_objects = []

        self.game_status = 0

        self.player = Player(self)
        ground = Ground()
        self.rendered_objects.append(ground)

        self.end_time = time.time() + self.GAME_LENGTH

        self.next_spawn_point = 0

        self.boss_obj = None
        self.magnet_obj = None

        self.keys = KBHit()
        clear_terminal_screen()

        self._loop()

    def _speed_powerup(self):
        config.FRAME_MOVE_SPEED *= 2

    def _get_time_remaining(self):
        time_remaining = (self.end_time - time.time())
        return int(np.round(time_remaining))

    def _info_print(self):
        # required padding since we are not clearing screen and just resetting carat pos
        padding = ' '*10
        print(
            f"Time remaining \u23f1 {self._get_time_remaining()} seconds{padding}")
        print(f"Lives remaining \u2764 {self.player.lifes}{padding}")
        print(f"Score {self.score}{padding}")

        if self.player.TYPE == "player":
            remain_time = self.player.get_remaining_shield_time()

            if self.player.shield_activated:
                print(f"Shield activated")
            elif remain_time:
                print(f"Shield available in {math.ceil(remain_time)} seconds")
            else:
                print("Shield available")

        if not self.boss_obj:
            print(
                f"Distance to boss {Boss.X_THRESHOLD - self.player.x}{padding}")
        else:
            print(f"Boss health: {max(0, self.boss_obj.health)}{padding}")

    def _draw(self):
        self.grid = np.array([[Fore.WHITE + Back.BLUE + " "
                               for _ in range(config.FRAME_WIDTH)]
                              for _ in range(config.FRAME_HEIGHT)])

        self._info_print()

        for obj in self.rendered_objects:
            info_objs = obj.draw()
            for info in info_objs:
                self._draw_in_range(info, obj.obj)

        self._draw_in_range(self.player.draw()[0], self.player.obj)
        # to avoid fringing
        padding = " " * 10
        # offset by 10: since otherwise the whole coin group disappears even if a
        # single coin touches the boundary
        grid_str = "\n".join([str(Style.RESET_ALL).join(row[10:]) + Style.RESET_ALL + padding
                              for row in self.grid])

        # only a single print at the end makes rendering efficient
        os.write(1, str.encode(grid_str))

    def _update(self):
        i = -1
        list_of_idxs_to_delete = []

        for obj in self.rendered_objects:
            i += 1
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
            if not self.magnet_obj and not self.boss_obj:
                if random.random() < Magnet.SPAWN_PROBABILITY:
                    self.magnet_obj = Magnet()
                    self.rendered_objects.append(self.magnet_obj)

    def _terminate(self, we_won):
        """
        user wants to terminate the game
        """
        self.game_status = -1
        print("\nGame over!")
        if we_won == 0:
            print("You lost!")
        elif we_won == 1:
            print("You won!")
        self._info_print()

        os.system('setterm -cursor on')

    def _handle_input(self):
        inputted = ""

        if self.keys.kbhit():
            inputted = self.keys.getch()

        cin = get_key_pressed(inputted)

        if cin == -1:
            self._terminate(-1)
        elif cin != 0:
            if cin in '1234' and config.DEBUG:
                if cin == '1':
                    self.rendered_objects.append(CoinGroup())
                if cin == '2':
                    self.magnet_obj = Magnet()
                    self.rendered_objects.append(self.magnet_obj)
                if cin == '3':
                    self.rendered_objects.append(FireBeam())

            if cin == 'b':
                laserList = self.player.fire_laser()
                for laser in laserList:
                    self.rendered_objects.append(laser)
            if cin == ' ' and self.player.TYPE == "player":
                self.player.activate_shield()

            if cin == 'y' and self.player.TYPE == "player":
                # replace player with dragon
                self.player = DragonPowerup(self)

        return cin

    def _loop(self):
        self.game_status = 1

        last_key_pressed = ""
        clear_terminal_screen()

        while self.game_status == 1:
            # switch to non terminal clearing later
            reposition_cursor()
            # clear_terminal_screen()

            if self.player.TYPE == "player" and config.DEBUG:
                debug_str = f"[{self.player.x} {self.player.y}] \
    [{self.player.x_vel} {self.player.y_vel}] \
    [{self.player.x_acc} {self.player.y_acc}]" + " " * 50

                print(debug_str)

            self._draw()
            self._update()
            self.player.update(last_key_pressed)

            if not self.boss_obj and self.player.x >= Boss.X_THRESHOLD:
                self.boss_obj = Boss(self)
                self.rendered_objects.append(self.boss_obj)
                # TODO: see other TODO comment
                if self.magnet_obj:
                    self.magnet_obj.destroy()

            last = time.time()
            last_key_pressed = self._handle_input()

            if self.player.lifes <= 0 or self._get_time_remaining() <= 0:
                self._terminate(0)
            if self.boss_obj and self.boss_obj.health <= 0:
                self._terminate(1)

            while time.time() - last < self._refresh_time:
                pass
