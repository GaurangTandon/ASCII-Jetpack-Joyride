"""
Boss related functions
"""

import random
import time
from colorama import Fore, Back
import config
from generic import GenericFrameObject


class Boss(GenericFrameObject):
    """
    Main enemy which the player needs to fight off
    """
    X_THRESHOLD = 1000  # comes out to be about 60secs
    Y_VEL = 1
    START_Y = round(config.FRAME_HEIGHT / 2)
    FIRE_INTERVAL = 1
    TYPE = "boss"

    # create an aura around him, basically make him a rectangular box to ease collision detection :P
    stringRepr = [
        "---------------",
        "|   /     \\   |",
        "|  ((     ))  |",
        "=   \\\\_v_//   =",
        "=====)_^_(=====",
        "====/ O O \\====",
        "== | /_ _\\ | ==",
        "|   \\/_ _\\/   |",
        "|    \\_ _/    |",
        "|    (o_o)    |",
        "|     VwV     |",
        "---------------"
    ]

    color = [Fore.WHITE, Back.RED]

    def __init__(self, game_obj):
        super().__init__()
        self.__y_vel = -1

        self._y = self.START_Y
        self._x = config.FRAME_SPAWN_X - 20

        self.__game_obj = game_obj

        self.__health = 100
        self.__last_fired = -1

    def _direction(self):
        return self.__game_obj._get_direction(self._y)

    def _fire_gun(self):
        boss_laser = BossLaser(
            self._x, self._y - self._height / 2, self.__game_obj)
        self.__game_obj.append_to_rendered_objects(boss_laser)

        self.__last_fired = time.time()

    def update(self):
        self.__y_vel = self._direction() * self.Y_VEL
        self._y += round(self.__y_vel)
        self._y = min(self._y, config.FRAME_BOTTOM_BOUNDARY)
        self._y = max(self._y, self._height)

        if time.time() - self.__last_fired >= self.FIRE_INTERVAL:
            self._fire_gun()

    def get_health(self):
        """
        getter
        """
        return self.__health

    def decrease_health(self, val):
        """
        setter
        """
        self.__health -= val


class BossLaser(GenericFrameObject):
    """
    Weapon fired by the main enemy
    """
    stringRepr = [
        "-^-",
        "<O>",
        "-v-"
    ]
    color = [Fore.WHITE, Back.BLUE]
    TYPE = "bosslaser"

    def _direction(self):
        """
        getter
        """
        return self.__game_obj._get_direction(self._y)

    def __init__(self, initX, initY, game_obj):
        super().__init__()

        self.__game_obj = game_obj
        self._y = initY
        self._x = initX

        self.vel_y = 1
        self.vel_x = -config.FRAME_MOVE_SPEED

    def update(self):
        # for a dragon player, guns should follow less since boss laser
        # is not ver specific
        if self.__game_obj.get_player_type() == "player":
            should_follow = 1 if random.random() <= 0.8 else -1
        else:
            should_follow = 1

        # get the player's coordinates and move towards it
        self._y += round(self.vel_y * self._direction() * should_follow)
        self._x += round(self.vel_x) * config.X_VEL_FACTOR

        self._y = max(self._y, self._height-1)
        self._y = min(self._y, config.FRAME_BOTTOM_BOUNDARY)

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG

        return False
