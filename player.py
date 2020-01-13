from math import sqrt
from colorama import Fore
import config
from generic import GenericFrameObject
from obstacle import Magnet


class Player(GenericFrameObject):
    startYCoord = config.FRAME_HEIGHT - config.GROUND_HEIGHT - 1
    # maintain rectangular shapes for ease of collision detection
    stringRepr = [
        "|/\\|",
        "|\\/|",
        "-||-",
        " || ",
        "----",
        "||||",
    ]
    color = [Fore.RED, None]

    def __init__(self, obj_game):
        super().__init__()

        # x and y coordinate of the player's leftmost bottommost point
        self.x = config.FRAME_LEFT_BOUNDARY
        self.y = self.startYCoord

        self.y_vel = 0
        self.x_vel = 0
        self.game_obj = obj_game

        self.x_acc = 0
        self.y_acc = 0

        self.w_key = False

        self.lifes = 3
        self.health = 100

    def get_top(self):
        return self.y - self.height + 1

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.y_vel += config.GRAVITY_ACC
        self.y_vel += self.y_acc

        if self.game_obj.magnet_obj:
            num = Magnet.FORCE_NUMERATOR
            x_dist = self.game_obj.magnet_obj.x - self.x
            y_dist = self.game_obj.magnet_obj.y - self.y
            hyp = sqrt(x_dist * x_dist + y_dist * y_dist)
            self.x_acc = x_dist / hyp * num
            self.y_acc = y_dist / hyp * num
        else:
            self.x_acc = 0
            self.y_acc = 0

        if self.w_key:
            self.y_acc += 0.15

        self.check_bounds()

    def reset_no_key(self):
        self.x_vel = 0

    def fire_laser(self):
        laser = Laser()

        laser.x = self.x
        laser.y = self.y

        return laser

    def update_key(self, key):
        if key not in 'ad':
            self.x_vel = 0

        if key != 'w':
            self.w_key = False

        # y_vel is set to zero in first two cases
        # such that player is still using jetpack
        if key == 'a':
            self.x_vel = -1
            self.y_vel = 0
        elif key == 'd':
            self.x_vel = 1
            self.y_vel = 0
        elif key == 'w':
            self.w_key = True
        elif key == ' ':
            return self.fire_laser()

        return None

    def check_bounds(self):
        # check sky bound
        self.y = max(self.y, self.height - 1)

        # check ground bound
        self.y = min(self.y, self.startYCoord)

        # can't move anymore
        if self.y >= self.startYCoord or self.y <= self.height - 1:
            self.y_vel = 0
            self.y_acc = 0

        # hack to not make the jetpack get stuck at the top
        if self.y <= self.height - 1:
            self.y += 0.01

        # TODO: the window should also move accordingly to accommodate
        if self.x >= config.FRAME_RIGHT_BOUNARY:
            self.x = config.FRAME_RIGHT_BOUNARY
            self.x_vel = 0

        if self.x <= config.FRAME_LEFT_BOUNDARY:
            self.x = config.FRAME_LEFT_BOUNDARY
            self.x_vel = 0

        for obj in self.game_obj.rendered_objects:
            pass
            # check collision
            # if self.collide(obj):
            #     if obj.isCoin:
            #         pass
            #     else:
            #         pass

        if self.lifes == 0:
            self.dead()


class Laser(GenericFrameObject):
    stringRepr = ["==>"]

    def update(self):
        self.x += config.LASER_VEL

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG

        return None
