"""
The ground, it can't be simpler
"""

import numpy as np
from colorama import Back
import config
from generic import GenericFrameObject


class Ground(GenericFrameObject):
    """
    The average boring rectangular ground
    """
    stringRepr = np.full(
        (config.GROUND_HEIGHT, config.FRAME_WIDTH), ' ')
    color = [None, Back.GREEN]
    TYPE = "ground"

    def __init__(self):
        super().__init__()
        self._x = 0
        self._y = config.FRAME_HEIGHT - 1

    def update(self):
        pass
