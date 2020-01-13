import numpy as np
from colorama import Back
import config
from generic import GenericFrameObject


class Ground(GenericFrameObject):
    stringRepr = np.full(
        (config.GROUND_HEIGHT, config.FRAME_WIDTH), ' ')
    color = [None, Back.GREEN]
    TYPE = "ground"

    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = config.FRAME_HEIGHT - 1

    def update(self):
        pass
