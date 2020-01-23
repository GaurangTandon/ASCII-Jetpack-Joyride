"""
Implementation of magnet and firebeam
"""

import time
import random
from colorama import Fore, Back
import config
from generic import GenericFrameObject, get_spawn_coordinates, GroupedObject


class FireBeam(GroupedObject):
    """
    The usual fire!
    """
    stringRepr = [" "]
    color = [Fore.RED, Back.RED]
    TYPE = "firebeam"
    damage = 10


def get_firebeam_group():
    """
    Returns a firebeam object of individual firebeams
    all having the same id
    """
    # enum {horizontal, vertical, diagonal}
    typer = random.randint(1, 3)
    objs = []
    c_x = 0
    c_y = 0

    if typer & 1:
        c_x = 1
    if typer & 2:
        c_y = 1

    x_coord, y_coord = get_spawn_coordinates(config.FIREBEAM_LENGTH)

    const_id = random.random()
    for _ in range(config.FIREBEAM_LENGTH):
        obj = FireBeam(x_coord, y_coord)

        x_coord += c_x
        y_coord -= c_y
        objs.append(obj)
        obj.set_id(const_id)

    return objs, config.FIREBEAM_LENGTH


class Magnet(GenericFrameObject):
    """
    That which won't leave you alone
    """
    stringRepr = [
        "MMMMM",
        "MM MM",
        "MM MM"
    ]
    color = [Fore.RED, Back.WHITE]
    LIFETIME = 10
    SPAWN_PROBABILITY = 0.005
    TYPE = "magnet"

    # magnetic attraction is modeled as Gm1m2/r^2 or Kq1q2/r^2 in real life
    # i have not added the r^2 term here, since it made the effect extremely bizzare
    FORCE_CONSTANT = 0.7

    def __init__(self):
        super().__init__()
        self.exists = True

        self._x = random.randint(
            config.FRAME_RIGHT_BOUNARY // 2 - 20, config.FRAME_RIGHT_BOUNARY // 2 + 20)

        top_half = random.randint(
            config.FRAME_HEIGHT // 4 - 5, config.FRAME_HEIGHT // 4 + 5)
        bottom_half = random.randint(
            3 * config.FRAME_HEIGHT // 4 - 5, 3 * config.FRAME_HEIGHT // 4 + 5)
        self._y = top_half if random.random() < 0.5 else bottom_half

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
