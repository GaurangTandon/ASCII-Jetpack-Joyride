"""
Coin group class
"""

import random
from colorama import Fore
from generic import get_spawn_coordinates, GroupedObject


class Coin(GroupedObject):
    """
    Coins occur in groups
    """
    TYPE = "coin"
    stringRepr = ["$"]
    color = [Fore.WHITE, None]


def get_coin_group():
    """
    Returns a group of coins sitting together
    """
    height = random.randint(3, 4)
    width = random.randint(3, 4)

    x_coord, y_coord = get_spawn_coordinates(height)

    lst = []
    for i in range(x_coord, x_coord + width):
        for j in range(y_coord - height + 1, y_coord + 1):
            coin_obj = Coin(i, j)
            lst.append(coin_obj)

    return lst, width
