import random
from colorama import Fore, Back
import config
from generic import GenericFrameObject


class FireBeam(GenericFrameObject):
    stringRepr = ["f"]
    color = [Fore.RED, None]

    def __init__(self):
        super().__init__()
        self.damage = 10
        # enum {horizontal, vertical, diagonal}
        self.type = random.randint(1, 3)

    def draw(self):
        objs = []
        # TODO: collide of laser with any one block should delete all five blocks of the firebeam
        c_x = 0
        c_y = 0

        if self.type & 1:
            c_x = 1
        if self.type & 2:
            c_y = 1

        x_coord = self.x
        y_coord = self.y

        for _ in range(config.FIREBEAM_LENGTH):
            info = {}
            info["coord"] = [y_coord, x_coord]
            info["size"] = [1, 1]
            x_coord += c_x
            y_coord += c_y
            objs.append(info)

        return objs


class Magnet(GenericFrameObject):
    stringRepr = [["MM"], ["MM"]]
    color = [Fore.RED, Back.WHITE]
