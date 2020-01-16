"""
Implementation of magnet and firebeam
"""

import time
import random
from colorama import Fore, Back
import config
from generic import GenericFrameObject


class FireBeam(GenericFrameObject):
    """
    Your usual fire!!
    """
    stringRepr = ["🔥"]
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
    """
    That which won't leave you alone
    """
    stringRepr = ["MM", "MM"]
    color = [Fore.RED, Back.WHITE]
    LIFETIME = 10
    SPAWN_PROBABILITY = 0.01
    TYPE = "magnet"

    # magnetic attraction is modeled as Gm1m2/r^2 or Kq1q2/r^2 in real life
    # i have not added the r^2 term here, since it made the effect extremely bizzare
    FORCE_CONSTANT = 50

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

        self.creation_time = time.time()

    def update(self):
        time_spent = time.time() - self.creation_time
        return None if time_spent < self.LIFETIME and self.exists else GenericFrameObject.DEAD_FLAG

    def destroy(self):
        """
        Destroy self, called by Game in extreme cases
        """
        self.exists = False

    def cleanup(self):
        return True
