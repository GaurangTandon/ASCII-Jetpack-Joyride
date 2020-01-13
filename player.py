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
    DRAG_CONSTANT = 0.1
    X_IMPULSE = 1
    Y_IMPULSE = 1

    def __init__(self, obj_game):
        super().__init__()

        # x and y coordinate of the player's leftmost bottommost point
        self.x = config.FRAME_LEFT_BOUNDARY
        self.y = self.startYCoord

        self.y_vel = 0
        self.x_vel = 0
        self.game_obj = obj_game

        self.y_acc = 0
        self.x_acc = 0

        self.w_key = False

        self.lifes = 3
        self.health = 100

    def get_top(self):
        return self.y - self.height + 1

    def update(self, last_key_pressed):
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

        # keypress gives an impulse, not an accn
        if last_key_pressed == 'w':
            self.y_vel -= self.Y_IMPULSE
        elif last_key_pressed == 'a':
            self.x_vel -= self.X_IMPULSE
        elif last_key_pressed == 'd':
            self.x_vel += self.X_IMPULSE

        self.y_vel += config.GRAVITY_ACC
        self.y_vel += self.y_acc
        self.x_vel += self.x_acc
        self.x_vel += (-1 if self.x_vel > 0 else 1) * min(self.DRAG_CONSTANT * self.x_vel *
                                                          self.x_vel, abs(self.x_vel))
        # self.x_vel += (-1 if self.x_vel > 0 else 1) * min(self.DRAG_CONSTANT * self.x_vel *
        #                                                   self.x_vel, abs(self.x_vel))

        self.x += round(self.x_vel)
        self.y += round(self.y_vel)

        self.check_bounds()

    def fire_laser(self):
        laser = Laser()

        laser.x = self.x
        laser.y = self.y

        return laser

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
