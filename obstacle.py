import config
import random
from generic import GenericFrameObject
from math import sqrt


class FireBeam(GenericFrameObject):
    stringRepr = ["f"]

    def __init__(self):
        super().__init__()
        self.damage = 10
        # enum {horizontal, vertical, diagonal}
        self.type = random.randint(1, 3)

    def draw(self):
        objs = []
        # TODO: collide with any one block should delete all five blocks of the firebeam
        cx = 0
        cy = 0

        if self.type & 1:
            cx = 1
        if self.type & 2:
            cy = 1

        x = self.x
        y = self.y

        for _ in range(config.FIREBEAM_LENGTH):
            info = {}
            info["coord"] = [x, y]
            info["size"] = [1, 1]
            x += cx
            y += cy
            objs.append(info)

        return objs


class Magnet(GenericFrameObject):
    stringRepr = [["M", "M"], ["M", "M"]]

    def __init__(self):
        super().__init__()
