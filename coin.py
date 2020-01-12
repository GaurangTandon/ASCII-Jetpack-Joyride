import random
import numpy as np
from colorama import Fore
from generic import GenericFrameObject


class CoinGroup(GenericFrameObject):
    """
    Coins occur in groups
    """
    color = [Fore.YELLOW, None]

    def __init__(self):
        self.height = random.randint(1, 2)
        self.width = random.randint(3, 4)
        super().__init__()
        self.obj = np.full((self.height, self.width), 'C')
