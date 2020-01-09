class Obstable:
    def __init__(self):
        pass


"""
TODO: this inheritance makes really no sense :/
"""


class FireBeam(Obstable):
    def __init__(self):
        super().__init__()
        self.damage = 10


class Magnet(Obstable):
    def __init__(self):
        self.damage = 0

    def draw(self):
        return {
            "objCode": 4,
        }
