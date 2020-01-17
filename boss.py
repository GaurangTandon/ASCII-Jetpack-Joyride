"""
Boss related functions
"""


import time
from colorama import Fore, Back
import config
from generic import GenericFrameObject


class Boss(GenericFrameObject):
    """
    Main enemy which the player needs to fight off
    """
    X_THRESHOLD = 15
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
        self.y_vel = -1

        self.y = self.START_Y
        self.x = config.FRAME_SPAWN_X

        self.game_obj = game_obj

        self.health = 100
        self.last_fired = -1

    def _direction(self):
        return (-1 if self.y > self.game_obj.player.y else 0 if self.y ==
                self.game_obj.player.y else 1)

    def _fire_gun(self):
        boss_laser = BossLaser(self.x, self.y - self.height / 2, self.game_obj)
        self.game_obj.rendered_objects.append(boss_laser)

        self.last_fired = time.time()

    def update(self):
        self.y_vel = self._direction() * self.Y_VEL
        self.y += round(self.y_vel)
        self.y = min(self.y, config.FRAME_BOTTOM_BOUNDARY)
        self.y = max(self.y, self.height)

        # get the player's coordinates and move towards it

        if time.time() - self.last_fired >= self.FIRE_INTERVAL:
            self._fire_gun()


class BossLaser(GenericFrameObject):
    """
    Weapon fired by the main enemy
    """
    stringRepr = [
        "-^-",
        "<O>",
        "-v-"
    ]
    color = [Fore.WHITE, Back.BLACK]
    TYPE = "bosslaser"

    def _direction(self):
        return (-1 if self.y > self.game_obj.player.y else 0 if self.y ==
                self.game_obj.player.y else 1)

    def __init__(self, initX, initY, game_obj):
        super().__init__()

        self.game_obj = game_obj
        self.y = initY
        self.x = initX

        self.vel_y = -1.5
        self.vel_x = -4

    def update(self):
        self.x += round(self.vel_x)

        self.vel_y += config.GRAVITY_ACC
        self.y += round(self.vel_y)
        self.y = max(self.y, self.height)

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG

        return False
