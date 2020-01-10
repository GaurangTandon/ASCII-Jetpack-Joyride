from colorama import Fore, Back, Style
import config
from generic import GenericFrameObject


class Player():
    def __init__(self):
        # x and y coordinate of the player's leftmost bottommost point
        self.x = 10
        self.y = 10
        self.width = config.PLAYER_WIDTH
        self.height = config.PLAYER_HEIGHT
        self.yVel = 0
        self.xVel = 0

        self.lifes = 3
        self.health = 100

    def update(self):
        self.x += self.xVel

        self.y += self.yVel
        self.yVel += config.GRAVITY_ACC

        self.checkBounds()

    def resetNoKey(self):
        self.xVel = 0

    def fireLaser(self):
        l = Laser()

        l.x = self.x
        l.y = self.y

        return l

    def updateKey(self, key):
        if key == 'a':
            self.xVel = -1
        elif key == 'd':
            self.xVel = 1
        elif key == 'w':
            self.yVel -= 1
        elif key == ' ':
            return self.fireLaser()
        else:
            assert(False)

    def checkBounds(self):
        # check sky bounds and ground bounds

        # check obstacle collision

        # check coin collision
        if self.lifes == 0:
            self.dead()

    def draw(self):
        return [{
            "cols": [self.x, self.x + self.width-1],
            "rows": [self.y - self.height, self.y],
            "objCode": config.GRID_CONSTS["player"]
        }]


class Laser(GenericFrameObject):
    def __init__(self):
        # x  and y set by caller
        self.x = -1
        self.y = -1

    def draw(self):
        return [{
            "objCode": config.GRID_CONSTS["playerlaser"],
            "cols": [self.x, self.x + config.LASER_WIDTH-1],
            "rows": [self.y - config.LASER_HEIGHT, self.y]
        }]

    def update(self):
        self.x += config.LASER_VEL
