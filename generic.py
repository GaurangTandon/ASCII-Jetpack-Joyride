"""
Module for generic frame object on render screen
"""
import random
from colorama import Fore
import numpy as np
import config
from util import tiler


def mapper(grid, height, width, color):
    """
    Maps a color array to the grid of height and width
    """
    assert len(grid[0]) == len(color[0])
    assert len(grid) == len(color)

    res = np.array([])

    for row in range(height):
        for col in range(width):
            curr_str = ""
            color_elm = color[row][col]

            if color_elm[0]:
                curr_str += color_elm[0]
            else:
                curr_str += Fore.BLACK

            if color_elm[1]:
                curr_str += color_elm[1]
            else:
                curr_str += config.BACK_COLOR

            curr_str += grid[row][col]
            res = np.append(res, curr_str)

    res = res.reshape((height, width))

    return res


class GenericFrameObject:
    """
    Generic frame object that can be rendered on the screen
    """
    currently_active = 0
    DEAD_FLAG = 1
    TYPE = "generic"

    def __init__(self):
        # this technique has been verified on this repl https://repl.it/@bountyhedge/mvce
        self.__class__.currently_active += 1
        self.__id = int(random.random() * 10000000)

        self._generate_draw_obj()

        self.x, self.y = get_spawn_coordinates(self.height)

    def get_id(self):
        return self.__id

    def set_id(self, val):
        self.__id = val

    def _generate_draw_obj(self):
        try:
            self.__class__.height = hgt = len(self.__class__.stringRepr)
            self.__class__.width = wdt = len(self.__class__.stringRepr[0])

            cond1 = len(self.__class__.color) != hgt
            cond2 = not isinstance(self.__class__.color[0], list) or len(
                self.__class__.color[0]) != wdt
            if cond1 or cond2:
                self.__class__.color = tiler(
                    self.__class__.color, hgt, wdt, True)

            self.__class__.obj = mapper(
                self.__class__.stringRepr, hgt, wdt, self.__class__.color)
        except AttributeError:
            pass

    def cleanup(self):
        """
        Any changes you may want to undo before getting destroyed
        """
        self.__class__.currently_active -= 1

    def draw(self):
        """
        Returns a dictionary containing sufficient info to draw
        """
        return [{
            "coord": [self.y, self.x],
            "size": [self.height, self.width]
        }]

    def get_type(self):
        """
        the TYPE variable is overriden by individual subclasses
        """
        return self.TYPE

    def exceeds_bounds(self):
        """
        If this object exceeds top or bottom bounds of the frame
        """
        return self.x < 0 or self.x + self.width > config.FRAME_WIDTH \
            or self.y > config.FRAME_BOTTOM_BOUNDARY or self.y < self.height

    def update(self):
        """
        Generic update function for moving things left
        """
        self.x -= config.FRAME_MOVE_SPEED * config.X_VEL_FACTOR

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG
        return None

    @staticmethod
    def _generate_coords(obj):
        points = set([])

        # both coordinates must be integers
        assert obj.y % 1 <= 1e-6
        assert obj.x % 1 <= 1e-6

        for i in range(int(obj.y) - obj.height + 1, int(obj.y) + 1):
            for j in range(int(obj.x), int(obj.x) + obj.width):
                points.add((i, j))

        return points

    # returns set of coordinates common to both objects
    def check_collision(self, obj):
        """
        Returns a set of points at which self and obj intersect
        """
        coords_self = GenericFrameObject._generate_coords(self)
        coords_obj = GenericFrameObject._generate_coords(obj)

        return coords_obj & coords_self


def get_spawn_coordinates(height):
    """
    Randomly return a valid spawn coordinate for things
    """
    return config.FRAME_SPAWN_X, random.randint(height, config.FRAME_BOTTOM_BOUNDARY)


class GroupedObject(GenericFrameObject):
    """
    Coins and firebeams that occur in groups
    """

    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

    def draw(self):
        return [{
            "coord": [self.y, self.x],
            "size": [1, 1]
        }]
