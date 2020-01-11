import config
import random
import numpy as np
from generic import GenericFrameObject

"""
Coins occur in groups
"""


class CoinGroup(GenericFrameObject):

    def __init__(self):
        super().__init__()
        self.height = random.randint(1, 2)
        self.width = random.randint(3, 4)
        self.obj = np.full((self.height, self.width), 'C')
