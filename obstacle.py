import config
import random
from generic import GenericFrameObject
from math import sqrt


class FireBeam(GenericFrameObject):
    def __init__(self):
        self.damage = 10
        # horizontal, vertical, diagonal
        self.type = random.randint(0, 2)
        self.x = 20
        self.y = 20

    def draw(self):
        info = {
            "objCode": config.GRID_CONSTS["firebeam"]
        }

        if self.type == 0:
            info["rows"] = [self.y, self.y]
            info["cols"] = [self.x, self.x + config.FIREBEAM_LENGTH - 1]
        elif self.type == 1:
            info["rows"] = [self.y - config.FIREBEAM_LENGTH + 1, self.y]
            info["cols"] = [self.x, self.x]
        else:
            dist = sqrt(config.FIREBEAM_LENGTH)
            info["rows"] = [self.y - dist + 1, self.y]
            info["cols"] = [self.x, self.x + dist - 1]

        return [info]


class Magnet():
    def __init__(self):
        pass

    def draw(self):
        return {
            "objCode": config.GRID_CONSTS["magnet"],
        }
