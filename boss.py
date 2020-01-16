from math import sqrt
import time
from colorama import Fore, Back
import random
import config
from generic import GenericFrameObject


class Boss(GenericFrameObject):
    X_THRESHOLD = 15
    Y_VEL = 0.5
    START_Y = round(config.FRAME_HEIGHT / 2)
    FIRE_INTERVAL = 2
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
        self.y_vel = 0

        self.y = self.START_Y
        self.x = config.FRAME_SPAWN_X

        self.game_obj = game_obj

        self.health = 100
        self.last_fired = -1

    def _direction(self):
        return (-1 if self.y > self.game_obj.player.y else 0 if self.y ==
                self.game_obj.player.y else 1)

    def fire_gun(self):
        # TODO: fix velocity to be better directed to the player

        self.game_obj.rendered_objects.append(
            BossLaser(self.x, self.y - self.height / 2, self.game_obj))

        self.last_fired = time.time()

    def update(self):
        self.y += round(self.y_vel)
        self.y = min(self.y, config.FRAME_BOTTOM_BOUNDARY)
        self.y = max(self.y, self.height)

        # get the player's coordinates and move towards it
        self.y_vel = self._direction() * self.Y_VEL

        if time.time() - self.last_fired >= self.FIRE_INTERVAL:
            self.fire_gun()


class BossLaser(GenericFrameObject):
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
        self.vel_y = 1
        self.vel_x = -2

    def update(self):
        self.x += round(self.vel_x)

        # with a probability, do not follow the player
        shouldFollow = 1 if random.random() <= 0.9 else -1

        self.y += round(self.vel_y * self._direction() * shouldFollow)

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG

        return False
