import config
import random


class GenericFrameObject:
    def __init__(self):
        self.x, self.y = self.getSpawnCoordinates()

    def update(self):
        self.x -= 1

    @classmethod
    def getSpawnCoordinates(self):
        return config.FRAME_RIGHT_BOUNARY + config.FRAME_SPAWN_OFFSET, random.randint(20, config.FRAME_HEIGHT-config.GROUND_HEIGHT)
