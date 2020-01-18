"""
Coin group class
"""

import random
import numpy as np
from colorama import Fore
from generic import GenericFrameObject, get_spawn_coordinates, GroupedObject


class Coin(GroupedObject):
    """
    Coins occur in groups
    """
    TYPE = "coin"
    stringRepr = ["C"]
    color = [Fore.WHITE, None]


def get_coin_group():
    height = random.randint(3, 4)
    width = random.randint(3, 4)

    x, y = get_spawn_coordinates(height)

    lst = []
    for i in range(x, x + width):
        for j in range(y - height + 1, y + 1):
            lst.append(Coin(i, j))
    return lst
