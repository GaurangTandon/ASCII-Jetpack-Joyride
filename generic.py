from colorama import Back, Fore
import config
import random
import numpy as np


def mapper(x, color):
    res = np.array([])

    for row in x:
        for col in row:
            s = ""
            if color[0]:
                s += color[0]
            else:
                s += Fore.BLACK

            if color[1]:
                s += color[1]
            else:
                s += Back.BLUE

            s += col
            res = np.append(res, s)

    res = res.reshape((len(x), len(x[0])))

    return res


class GenericFrameObject:
    currentlyActive = 0
    DEAD_FLAG = 1

    def __init__(self):
        self.x, self.y = self.getSpawnCoordinates()
        # this technique has been verified on this repl https://repl.it/@bountyhedge/mvce
        self.__class__.currentlyActive += 1

        try:
            self.height = len(self.__class__.stringRepr)
            self.width = len(self.__class__.stringRepr[0])

            self.__class__.obj = mapper(
                self.__class__.stringRepr, self.__class__.color)

        except AttributeError:
            pass

    def cleanup(self):
        self.__class__.currentlyActive -= 1

    def draw(self):
        return [{
            "coord": [self.y, self.x],
            "size": [self.height, self.width]
        }]

    @classmethod
    def spawnProbability(self):
        try:
            ca = self.currentlyActive

            # TODO: improve random spawning, still not nice
            ca2 = ca*ca
            ca4 = ca2*ca2

            return 1 / ca4
        except ArithmeticError:
            return 0.1

    def update(self):
        self.x -= 1
        if self.x < 0:
            return GenericFrameObject.DEAD_FLAG

    @classmethod
    def getSpawnCoordinates(self):
        return config.FRAME_SPAWN_X, random.randint(20, config.FRAME_HEIGHT-config.GROUND_HEIGHT)
