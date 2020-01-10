import config
import random
from generic import GenericFrameObject


class Coin(GenericFrameObject):
    def __init__(self):
        self.value = config.COIN_VALUE
        # coordinates of bottom part
        self.x = -1
        self.y = -1

    def draw(self):
        return [{
            "objCode": config.GRID_CONSTS["coin"],
            "rows": [self.y - config.COIN_HEIGHT + 1, self.y],
            "cols": [self.x, self.x + config.COIN_WIDTH-1]
        }]


"""
Coins occur in groups
"""


class CoinGroup:
    def __init__(self):
        self.vSize = random.randint(1, 2)
        self.hSize = random.randint(3, 4)
        self.coins = []
        # todo: should be randomly decided
        self.xCoord = 0
        self.yCoord = 0

        # vertical size is always 2 :/
        print(self.vSize, self.hSize)
        x, y = self.xCoord, self.yCoord
        for row in range(self.vSize):
            for col in range(self.hSize):
                c = Coin()
                c.x = x
                c.y = y
                self.coins.append(c)
                x += config.COIN_WIDTH

            x = self.xCoord
            y += config.COIN_HEIGHT

    def draw(self):
        infos = []

        for coin in self.coins:
            infos.extend(coin.draw())

        return infos

    def update(self):
        for coin in self.coins:
            coin.update()
