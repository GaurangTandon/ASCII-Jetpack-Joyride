from colorama import Fore, Back, Style
from util import GRID_CONSTS


class Player():
    # x and y coordinate of the player's bottommost point
    x = -1
    y = -1

    def __init__(self):
        self.x = 50
        self.y = 50
        self.width = 10
        self.height = 10

    def draw(self, grid):
        for x in range(self.x, self.x + self.width):
            for y in range(self.y, self.y + self.height):
                grid[x][y] = GRID_CONSTS["player"]
