import config
import random


class Coin:
    def __init__(self, *args, **kwargs):
        self.value = config.COIN_VALUE

    def draw(self):


"""
Coins occur in groups
"""


class CoinGroup:
    def __init__(self):
        self.vSize = random.randint(1, 2)
        self.hSize = random.randint(3, 4)

    def draw(self):
        pass
