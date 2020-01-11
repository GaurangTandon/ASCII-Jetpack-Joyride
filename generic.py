import config
import random
import numpy as np


class GenericFrameObject:
    currentlyActive = 0

    def __init__(self):
        self.x, self.y = self.getSpawnCoordinates()
        # this technique has been verified on this repl https://repl.it/@bountyhedge/mvce
        self.__class__.currentlyActive += 1

        try:
            self.height = len(self.__class__.stringRepr)
            self.width = len(self.__class__.stringRepr[0])

            self.__class__.obj = np.array(
                self.__class__.stringRepr).reshape((self.height, self.width))
        except AttributeError:
            # stringRepr doesn't exist
            pass

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

    @classmethod
    def getSpawnCoordinates(self):
        return config.FRAME_RIGHT_BOUNARY + config.FRAME_SPAWN_OFFSET, random.randint(20, config.FRAME_HEIGHT-config.GROUND_HEIGHT)
