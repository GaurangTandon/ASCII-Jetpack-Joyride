import config


class FireBeam():
    def __init__(self):
        self.damage = 10


class Magnet():
    def __init__(self):

    def draw(self):
        return {
            "objCode": config.GRID_CONSTS["magnet"],
        }
