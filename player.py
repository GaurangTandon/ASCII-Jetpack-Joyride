from colorama import Fore, Back, Style
import config
from generic import GenericFrameObject
from ground import Ground
import numpy


class Player(GenericFrameObject):
    startYCoord = config.FRAME_HEIGHT - config.GROUND_HEIGHT - 1
    # maintain rectangular shapes for ease of collision detection
    stringRepr = [
        ["|", "/", "\\", "|"],
        ["|", "\\", "/", "|"],
        ["-", "|", "|", "-"],
        [" ", "|", "|", " "],
        ["-", "-", "-", "-"],
        ["|", "|", "|", "|"]
    ]
    color = [Fore.RED, None]

    def __init__(self):
        super().__init__()

        # x and y coordinate of the player's leftmost bottommost point
        self.x = config.FRAME_LEFT_BOUNDARY
        self.y = self.startYCoord

        self.yVel = 0
        self.xVel = 0

        self.lifes = 3
        self.health = 100

    def getTop(self):
        return self.y - self.height + 1

    def update(self):
        self.x += self.xVel

        self.y += self.yVel
        self.yVel += config.GRAVITY_ACC

        # self.x = round(self.x)
        # self.y = round(self.y)

        self.checkBounds()

    def resetNoKey(self):
        self.xVel = 0

    def fireLaser(self):
        l = Laser()

        l.x = self.x
        l.y = self.y

        return l

    def updateKey(self, key):
        if key not in 'ad':
            self.xVel = 0

        if key == 'a':
            self.xVel = -1
        elif key == 'd':
            self.xVel = 1
        elif key == 'w':
            # makes controls very hard to use
            self.yVel -= 2
            self.yVel = max(-3, self.yVel)
            self.yVel = min(1, self.yVel)
        elif key == ' ':
            return self.fireLaser()
        else:
            assert(False)

    def checkBounds(self):
        # check sky bound
        self.y = max(self.y, self.height - 1)

        # check ground bound
        self.y = min(self.y, self.startYCoord)

        # can't move anymore
        if self.y == self.startYCoord or self.y == self.height - 1:
            self.yVel = 0

        # hack to not make the jetpack get stuck at the top
        if self.y == self.height - 1:
            self.y += 0.01

        # TODO: the window should also move accordingly to accommodate
        if self.x >= config.FRAME_RIGHT_BOUNARY:
            self.x = config.FRAME_RIGHT_BOUNARY
            self.xVel = 0

        if self.x <= config.FRAME_LEFT_BOUNDARY:
            self.x = config.FRAME_LEFT_BOUNDARY
            self.xVel = 0

        # check obstacle collision

        # check coin collision
        if self.lifes == 0:
            self.dead()


class Laser(GenericFrameObject):
    stirngRepr = ["=", "=", ">"]

    def __init__(self):
        super().__init__()

    def update(self):
        self.x += config.LASER_VEL
