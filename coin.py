import config
import random
from generic import GenericFrameObject


class Coin(GenericFrameObject):
    def __init__(self):
        self.value = config.COIN_VALUE
        # coordinates of left bottom part
        self.x = -1
        self.y = -1
        self.width = 1
        self.height = 1

    def draw(self):
        return [{
            "objCode": config.GRID_CONSTS["coin"],
            "rows": [self.y - self.height + 1, self.y],
            "cols": [self.x, self.x + self.width - 1]
        }]


"""
Coins occur in groups
"""


class CoinGroup(GenericFrameObject):

    def __init__(self):
        super().__init__()
        self.vSize = random.randint(1, 2)
        self.hSize = random.randint(3, 4)
        self.coins = []
        # todo: should be randomly decided
        x = self.x
        y = self.y

        for row in range(self.vSize):
            for col in range(self.hSize):
                c = Coin()
                c.x = x
                c.y = y
                self.coins.append(c)
                x += c.width

            x = self.x
            y += c.height

    def draw(self):
        infos = []

        for coin in self.coins:
            infos.extend(coin.draw())

        return infos

    def update(self):
        for coin in self.coins:
            coin.update()
