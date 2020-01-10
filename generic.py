import config
import random


class GenericFrameObject:
    currentlyActive = 0

    def __init__(self):
        self.x, self.y = self.getSpawnCoordinates()
        # this technique has been verified on this repl https://repl.it/@bountyhedge/mvce
        self.__class__.currentlyActive += 1

    @classmethod
    def spawnProbability(self):
        try:
            ca = self.currentlyActive

            return 1 / (ca*ca*ca)
        except ArithmeticError:
            return 0.1

    def update(self):
        self.x -= 1

    @classmethod
    def getSpawnCoordinates(self):
        return config.FRAME_RIGHT_BOUNARY + config.FRAME_SPAWN_OFFSET, random.randint(20, config.FRAME_HEIGHT-config.GROUND_HEIGHT)
