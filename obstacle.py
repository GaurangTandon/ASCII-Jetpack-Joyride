import config
import random
from generic import GenericFrameObject
from math import sqrt


class FireBeam(GenericFrameObject):
    def __init__(self):
        self.damage = 10
        # horizontal, vertical, diagonal
        self.type = random.randint(0, 2)
        self.x = 20
        self.y = 20

    def _getInfo(self):
        return {"objCode": config.GRID_CONSTS["firebeam"]}

    def draw(self):
        objs = []
        info = self._getInfo()

        if self.type == 0:
            info["rows"] = [self.y, self.y]
            info["cols"] = [self.x, self.x + config.FIREBEAM_LENGTH - 1]
            objs.append(info)
        elif self.type == 1:
            info["rows"] = [self.y - config.FIREBEAM_LENGTH + 1, self.y]
            info["cols"] = [self.x, self.x]
            objs.append(info)
        else:
            x = self.x
            y = self.y

            for _ in range(config.FIREBEAM_LENGTH):
                info = self._getInfo()
                info["cols"] = [x, x]
                info["rows"] = [y, y]
                x += 1
                y + """  """ = 1
                objs.append(info)

        return objs


class Magnet():
    def __init__(self):
        pass

    def draw(self):
        return {
            "objCode": config.GRID_CONSTS["magnet"],
        }
