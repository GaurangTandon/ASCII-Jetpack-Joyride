import random
import numpy as np
from colorama import Fore
from generic import GenericFrameObject


class CoinGroup(GenericFrameObject):
    """
    Coins occur in groups
    """
    TYPE = "coin"

    def __init__(self):
        self.height = random.randint(3, 4)
        self.width = random.randint(3, 4)
        super().__init__()
        self.obj = np.full((self.height, self.width), 'C')
        self.color = [Fore.YELLOW, None]
