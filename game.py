"""
The actual game and rendering related functions
"""


import os
import sys
import random
import math
import time
import numpy as np
from colorama import init as coloramaInit, Fore, Style
from player import Player
from kbhit import KBHit
from util import clear_terminal_screen, get_key_pressed, reposition_cursor
import config
from config import FRAME_RATE
from ground import Ground
from coin import get_coin_group
from obstacle import get_firebeam_group, Magnet
from generic import GenericFrameObject
from boss import Boss
from powerup import DragonPowerup
from extras import Mountain, Cloud


class Game():
    """
    The actual game and rendering related functions
    """
    _refresh_time = 1 / FRAME_RATE
    GAME_LENGTH = 120
    SPEED_TIME = 10

    # info bounding indices are inclusive

    def _draw_in_range(self, info, obj):
        to_row = round(info["coord"][0])
        from_row = to_row - info["size"][0] + 1

        from_col = round(info["coord"][1])
        to_col = from_col + info["size"][1] - 1

        self.__grid[from_row: to_row + 1,
                    from_col:to_col + 1] = obj

    def __init__(self):
        coloramaInit()

        self.__score = 0
        self.__ticks = 0

        self.__grid = [[]]
        self.__rendered_objects = []

        self.__game_status = 0

        self.__player = Player(self)
        ground = Ground()
        self.__rendered_objects.append(ground)

        self.__end_time = time.time() + self.GAME_LENGTH

        self.__next_spawn_ticks = 0

        self.__boss_obj = None
        self.__magnet_obj = None

        self.__speed_on_time = -1
        self.__delete_id_list = []

        self.__x_travelled = 0

        self.__keys = KBHit()
        clear_terminal_screen()

        self._loop()

    @classmethod
    def speed_powerup(cls, activate=True):
        """
        Activation or deactivation of the speed powerup
        """
        factor = 2
        if activate:
            config.FRAME_MOVE_SPEED *= factor
        else:
            config.FRAME_MOVE_SPEED //= factor

    def is_sped_up(self):
        """
        Checks if the game has speed powerup
        """
        return self.__speed_on_time > 0

    def _info_print(self):
        # required padding since we are not clearing screen and just resetting carat pos
        padding = ' '*10
        print(
            f"Time remaining \u23f1 {self._get_time_remaining()} seconds{padding}")
        print(f"Lives remaining \u2764 {self.__player.get_lives()}{padding}")
        print(f"Score {self.get_score()}{padding}")

        if self.__player.get_type() == "player":
            remain_time = self.__player.get_remaining_shield_time()

            if self.__player.get_shield_activated():
                remain = Player.SHIELD_TIME - \
                    int(time.time() - self.__player.get_last_used_shield())
                print(
                    f"Shield time remaining: {remain}{padding}")
            elif remain_time:
                print(f"Shield available in {math.ceil(remain_time)} seconds")
            else:
                print(f"Shield available{padding}")

        if self.is_sped_up():
            trm = int(self.SPEED_TIME - (time.time() - self.__speed_on_time))
            print(f"Game sped up for {trm}!{padding}")
        else:
            print(f"Game at normal speed")

        if not self.__boss_obj:
            distance = (Boss.X_THRESHOLD -
                        self.get_x_travelled())

            print(f"Distance to boss {distance}{padding}")
        else:
            print(
                f"Boss health: {max(0, self.__boss_obj.get_health())}{padding}")

    def _draw(self):
        self.__grid = np.array([[Fore.WHITE + config.BACK_COLOR + " "
                                 for _ in range(config.FRAME_WIDTH)]
                                for _ in range(config.FRAME_HEIGHT)])

        self._info_print()

        for obj in self.get_rendered_objects():
            info_objs = obj.draw()
            for info in info_objs:
                self._draw_in_range(info, obj.obj)

        self._draw_in_range(self.__player.draw()[0], self.__player.obj)
        # to avoid fringing
        padding = " " * 10
        # offset by 10: since otherwise the whole coin group disappears even if a
        # single coin touches the boundary
        sra = str(Style.RESET_ALL)
        ender = sra + padding
        start = config.FRAME_LEFT_BOUNDARY
        end = config.FRAME_RIGHT_BOUNARY
        grid_str = "\n".join(
            [sra.join(row[start:end+1]) + ender for row in self.get_grid()])

        # only a single print at the end makes rendering efficient
        os.write(1, str.encode(grid_str))

    def _delete_objects(self):
        for i in range(len(self.__rendered_objects) - 1, -1, -1):
            obj = self.__rendered_objects[i]
            if not obj.get_id() in self.__delete_id_list:
                continue

            if obj.cleanup():
                self.__magnet_obj = None

            self.__rendered_objects.pop(i)

    def _update(self):
        self.__ticks += config.X_VEL_FACTOR
        self.set_x_travelled(self.get_x_travelled() + config.X_VEL_FACTOR)

        # use insert(0) since these objects should render before all other objects
        if self.__ticks % 75 == 0:
            self.__rendered_objects.insert(0, Cloud())

        if self.__ticks % 100 == 0:
            self.__rendered_objects.insert(0, Mountain())

        for obj in self.__rendered_objects:
            if obj.update() == GenericFrameObject.DEAD_FLAG:
                assert obj.get_id() is not None
                self.__delete_id_list.append(obj.get_id())

        # make spawning random somehow
        # make two slots in y axis as well
        if not config.DEBUG:
            if self.__ticks > self.__next_spawn_ticks:
                for random_spawn in [get_coin_group, get_firebeam_group]:
                    threshold = 0.05

                    if random.random() < threshold:
                        objs, width = random_spawn()
                        for obj in objs:
                            self.__rendered_objects.append(obj)

                        self.__next_spawn_ticks = max(
                            self.__next_spawn_ticks, self.__ticks + obj.width)

                        break

            if not self.__magnet_obj and not self.__boss_obj:
                if random.random() < Magnet.SPAWN_PROBABILITY:
                    self.__magnet_obj = Magnet()
                    self.__rendered_objects.append(self.__magnet_obj)

        if self.is_sped_up() and time.time() - self.__speed_on_time >= self.SPEED_TIME:
            self.speed_powerup(False)
            # can only use once
            self.__speed_on_time = -2
            config.X_VEL_FACTOR = 1

    def _terminate(self, we_won):
        """
        user wants to terminate the game
        """
        self.__game_status = -1
        print("\nGame over!")
        if we_won == 0:
            print("You lost!")
        elif we_won == 1:
            print("You won!")
        self._info_print()

        os.system('setterm -cursor on')

    def _handle_input(self):
        inputted = ""

        if self.__keys.kbhit():
            inputted = self.__keys.getch()

        cin = get_key_pressed(inputted)

        if cin == -1:
            self._terminate(-1)
        elif str(cin) in '1234' and config.DEBUG:
            if cin == '1':
                objs = get_coin_group()
                for obj in objs:
                    self.__rendered_objects.append(obj)
            if cin == '2':
                self.__magnet_obj = Magnet()
                self.__rendered_objects.append(self.__magnet_obj)
            if cin == '3':
                objs = get_firebeam_group()
                for obj2 in objs:
                    self.__rendered_objects.append(obj2)
        elif cin == 'b':
            laser_list = self.__player.fire_laser()
            for laser in laser_list:
                self.__rendered_objects.append(laser)
        elif cin == ' ' and self.__player.get_type() == "player":
            self.__player.activate_shield()
        elif cin == 'y' and self.__player.get_type() == "player":
            # replace player with dragon
            self.__player = DragonPowerup(self)
            Boss.FIRE_INTERVAL = 0.75
        elif cin == 't' and not self.is_sped_up():
            self.speed_powerup()
            self.__speed_on_time = time.time()
            config.X_VEL_FACTOR = 2

        return cin

    def _loop(self):
        self.__game_status = 1

        last_key_pressed = ""
        clear_terminal_screen()

        while self.__game_status == 1:
            # switch to non terminal clearing later
            reposition_cursor()
            # clear_terminal_screen()

            self.__delete_id_list = []
            self._draw()
            self._update()
            self.__player.update(last_key_pressed)
            self._delete_objects()

            if not self.__boss_obj and self.__x_travelled >= Boss.X_THRESHOLD:
                self.__boss_obj = Boss(self)
                self.__rendered_objects.append(self.__boss_obj)

                if self.__magnet_obj:
                    self.__magnet_obj.destroy()

            last = time.time()
            last_key_pressed = self._handle_input()

            if self.__player.get_lives() <= 0 or self._get_time_remaining() <= 0:
                self._terminate(0)
            if self.__boss_obj and self.__boss_obj.get_health() <= 0:
                self._terminate(1)

            while time.time() - last < self._refresh_time:
                sys.stdin.flush()
                sys.stdout.flush()
                pass

    def set_speed_on_time(self, val):
        """
        setter
        """
        self.__speed_on_time = val
        config.X_VEL_FACTOR = 2

    def append_to_delete_list(self, idd):
        """
        setter
        """
        self.__delete_id_list.append(idd)

    def increment_score(self):
        """
        setter
        """
        self.__score += 1

    def get_rendered_objects(self):
        """
        getter
        """
        return self.__rendered_objects

    def decrement_player_bullets(self):
        """
        setter
        """
        self.__player.decrement_bullets()

    def get_player_type(self):
        """
        getter
        """
        return self.__player.get_type()

    def decrement_boss_health(self, val):
        """
        setter
        """
        self.__boss_obj.decrease_health(val)

    def get_magnet_coords(self):
        """
        getter
        """
        return (None, None) if not self.__magnet_obj else (self.__magnet_obj.x, self.__magnet_obj.y)

    def get_end_time(self):
        """
        getter
        """
        return self.__end_time

    def _get_time_remaining(self):
        time_remaining = (self.get_end_time() - time.time())
        return int(np.round(time_remaining))

    def get_score(self):
        """
        getter
        """
        return self.__score

    def get_x_travelled(self):
        """
        getter
        """
        return self.__x_travelled

    def get_grid(self):
        """
        getter
        """
        return self.__grid

    def set_x_travelled(self, val):
        """
        setter
        """
        self.__x_travelled = val

    def inc_score(self, val):
        self.__score += val

    def get_rendered_objects(self):
        return self.__rendered_objects

    def append_to_rendered_objects(self, val):
        self.__rendered_objects.append(val)

    def _get_direction(self, y_coord):
        return (-1 if y_coord > self.__player.y else 0 if y_coord ==
                self.__player.y else 1)
