from colorama import Fore, Back, Style
import config


class Player():
    # x and y coordinate of the player's bottommost point
    x = -1
    y = -1

    def __init__(self):
        self.x = 10
        self.y = 10
        self.width = config.PLAYER_WIDTH
        self.height = config.PLAYER_HEIGHT
        self.yVel = 0
        self.xVel = 0

    def update(self):
        self.y += self.yVel
        self.yVel += config.GRAVITY_ACC
        self.checkBounds()

    def checkBounds(self):
        # check sky bounds and ground bounds

        # check obstacle collision

        # check coin collision

    def draw(self):
        return {
            "from_row": self.x - self.height,
            "to_row": self.x,
            "from_col": self.y,
            "to_col": self.y + self.width,
            "objCode": config.GRID_CONSTS["player"]
        }
