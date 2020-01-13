import random
from colorama import Fore, Back
from util import Timer
import config
from generic import GenericFrameObject


class FireBeam(GenericFrameObject):
    stringRepr = ["f"]
    color = [Fore.RED, None]
    TYPE = "firebeam"

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
            y_coord -= c_y
            objs.append(info)

        return objs


class Magnet(GenericFrameObject):
    stringRepr = ["MM", "MM"]
    color = [Fore.RED, Back.WHITE]
    LIFETIME = 10
    SPAWN_PROBABILITY = 0.01
    TYPE = "magnet"

    # magnetic attraction is modeled as Gm1m2/r^2 or Kq1q2/r^2
    FORCE_NUMERATOR = 1

    def __init__(self):
        super().__init__()
        self.exists = True

        self.x = random.randint(
            config.FRAME_RIGHT_BOUNARY // 2 - 20, config.FRAME_RIGHT_BOUNARY // 2 + 20)

        top_half = random.randint(
            config.FRAME_HEIGHT // 4 - 5, config.FRAME_HEIGHT // 4 + 5)
        bottom_half = random.randint(
            3 * config.FRAME_HEIGHT // 4 - 5, 3 * config.FRAME_HEIGHT // 4 + 5)
        self.y = top_half if random.random() < 0.5 else bottom_half

        timer = Timer()
        timer.set_timeout(self.destroy, self.LIFETIME)

    def update(self):
        return None if self.exists else GenericFrameObject.DEAD_FLAG

    def cleanup(self):
        return True

    def destroy(self):
        self.exists = False
