import config
import random
import numpy as np
from generic import GenericFrameObject
from colorama import Fore, Back

"""
Coins occur in groups
"""


class CoinGroup(GenericFrameObject):
    color = [Fore.YELLOW, None]

    def __init__(self):
        self.height = random.randint(1, 2)
        self.width = random.randint(3, 4)
        super().__init__()
        self.obj = np.full((self.height, self.width), 'C')
