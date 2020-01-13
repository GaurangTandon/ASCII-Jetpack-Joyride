import random
from colorama import Back, Fore
import numpy as np
import config


def mapper(grid, color):
    res = np.array([])

    for row in grid:
        for col in row:
            curr_str = ""
            if color[0]:
                curr_str += color[0]
            else:
                curr_str += Fore.BLACK

            if color[1]:
                curr_str += color[1]
            else:
                curr_str += Back.BLUE

            curr_str += col
            res = np.append(res, curr_str)

    res = res.reshape((len(grid), len(grid[0])))

    return res


class GenericFrameObject:
    currentlyActive = 0
    DEAD_FLAG = 1

    def __init__(self):
        # this technique has been verified on this repl https://repl.it/@bountyhedge/mvce
        self.__class__.currentlyActive += 1

        try:
            self.__class__.height = len(self.__class__.stringRepr)
            self.__class__.width = len(self.__class__.stringRepr[0])

            self.__class__.obj = mapper(
                self.__class__.stringRepr, self.__class__.color)
        except AttributeError:
            pass

        self.x, self.y = self.get_spawn_coordinates()

    def cleanup(self):
        self.__class__.currentlyActive -= 1

    def draw(self):
        return [{
            "coord": [self.y, self.x],
            "size": [self.height, self.width]
        }]

    @classmethod
    def spawn_probability(self):
        try:
            c_a = self.currentlyActive

            # TODO: improve random spawning, still not nice
            ca2 = c_a*c_a
            ca4 = ca2*ca2

            return 1 / ca4
        except ArithmeticError:
            return 0.1

    def exceeds_bounds(self):
        return self.x < 0 or self.x >= config.FRAME_WIDTH \
            or self.y >= config.FRAME_BOTTOM_BOUNDARY or self.y <= self.height

    def update(self):
        self.x -= config.FRAME_MOVE_SPEED

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG
        return None

    def get_spawn_coordinates(self):
        return config.FRAME_SPAWN_X, random.randint(self.height, config.FRAME_BOTTOM_BOUNDARY)

    def check_collision(self, object):
        pass
