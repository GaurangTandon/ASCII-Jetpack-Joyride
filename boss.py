from math import sqrt
import time
from colorama import Fore, Back

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
        x_dist = abs(self.x - self.game_obj.player.x)
        y_dist = abs(self.y - self.game_obj.player.y)
        hyp = sqrt(x_dist * x_dist + y_dist * y_dist)
        vel = 2

        velx = vel * x_dist / hyp
        vely = vel * y_dist / hyp

        vely = self._direction() * vely

        self.game_obj.rendered_objects.append(
            BossLaser(vely, -velx, self.x, self.y - self.height / 2))

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

    def __init__(self, initvy, initvx, initX, initY):
        super().__init__()

        self.y = initY
        self.x = initX
        self.vel_y = initvy
        self.vel_x = initvx

    def update(self):
        self.x += round(self.vel_x)
        self.y += round(self.vel_y)

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG

        return False
