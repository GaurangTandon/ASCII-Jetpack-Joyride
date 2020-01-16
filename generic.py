"""
Module for generic frame object on render screen
"""
import random
from colorama import Back, Fore
import numpy as np
import config
from util import tiler


def mapper(grid, hgt, wdt, color):
    res = np.array([])

    for row in range(hgt):
        for col in range(wdt):
            curr_str = ""
            color_elm = color[row][col]

            if color_elm[0]:
                curr_str += color_elm[0]
            else:
                curr_str += Fore.BLACK

            if color_elm[1]:
                curr_str += color_elm[1]
            else:
                curr_str += Back.BLUE

            curr_str += grid[row][col]
            res = np.append(res, curr_str)

    res = res.reshape((hgt, wdt))

    return res


class GenericFrameObject:
    """
    Generic frame object that can be rendered on the screen
    """
    currently_active = 0
    DEAD_FLAG = 1

    def __init__(self):
        # this technique has been verified on this repl https://repl.it/@bountyhedge/mvce
        self.__class__.currently_active += 1

        self._generate_draw_obj()

        self.x, self.y = self.get_spawn_coordinates()

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
        self.__class__.currently_active -= 1

    def draw(self):
        return [{
            "coord": [self.y, self.x],
            "size": [self.height, self.width]
        }]

    @classmethod
    def spawn_probability(cls):
        try:
            c_a = cls.currently_active

            # TODO: improve random spawning, still not nice
            ca2 = c_a*c_a
            ca4 = ca2*ca2

            return 1 / ca4
        except ArithmeticError:
            return 0.1

    def exceeds_bounds(self):
        return self.x < 0 or self.x + self.width > config.FRAME_WIDTH \
            or self.y > config.FRAME_BOTTOM_BOUNDARY or self.y < self.height

    def update(self):
        self.x -= config.FRAME_MOVE_SPEED

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG
        return None

    def get_spawn_coordinates(self):
        return config.FRAME_SPAWN_X, random.randint(self.height, config.FRAME_BOTTOM_BOUNDARY)

    # TODO: is this private?
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
        coords_self = GenericFrameObject._generate_coords(self)
        coords_obj = GenericFrameObject._generate_coords(obj)

        return coords_obj & coords_self
