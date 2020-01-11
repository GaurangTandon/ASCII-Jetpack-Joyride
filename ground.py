import numpy as np
import config
from generic import GenericFrameObject
from colorama import Back


class Ground(GenericFrameObject):
    stringRepr = np.full(
        (config.GROUND_HEIGHT, config.FRAME_WIDTH), ' ')
    color = [None, Back.GREEN]

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = config.FRAME_HEIGHT - 1

    def update(self):
        pass
