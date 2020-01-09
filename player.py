from colorama import Fore, Back, Style
import config


class Player():
    def __init__(self):
        # x and y coordinate of the player's bottommost point
        self.x = 10
        self.y = 0
        self.width = config.PLAYER_WIDTH
        self.height = config.PLAYER_HEIGHT
        self.yVel = 0
        self.xVel = 0

        self.lifes = 3

    def update(self):
        self.x += self.xVel

        self.y += self.yVel
        self.yVel += config.GRAVITY_ACC

        self.checkBounds()

    def resetNoKey(self):
        self.xVel = 0

    def fireGun(self):
        pass

    def updateKey(self, key):
        if key == 'a':
            self.xVel = -1
        elif key == 'd':
            self.xVel = 1
        elif key == 'w':
            self.yVel += 1
        elif key == ' ':
            self.fireGun()
        else:
            assert(False)

    def checkBounds(self):
        pass
        # check sky bounds and ground bounds

        # check obstacle collision

        # check coin collision
        if self.lifes == 0:
            self.dead()

    def draw(self):
        return {
            "from_col": self.x - self.height,
            "to_col": self.x,
            "from_row": self.y,
            "to_row": self.y + self.width,
            "objCode": config.GRID_CONSTS["player"]
        }
