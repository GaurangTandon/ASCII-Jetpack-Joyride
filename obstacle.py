import config
import random
from generic import GenericFrameObject
from math import sqrt


class FireBeam(GenericFrameObject):

    def __init__(self):
        super().__init__()
        self.damage = 10
        # enum {horizontal, vertical, diagonal}
        self.type = random.randint(0, 2)

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
            # collision detection :/
            x = self.x
            y = self.y

            for _ in range(config.FIREBEAM_LENGTH):
                info = self._getInfo()
                info["cols"] = [x, x]
                info["rows"] = [y, y]
                x += 1
                y += 1
                objs.append(info)

        return objs


class Magnet(GenericFrameObject):

    def __init__(self):
        super().__init__()

    def draw(self):
        return [{
            "objCode": config.GRID_CONSTS["magnet"],
            "cols": [self.x, self.x + config.MAGNET_LENGTH - 1],
            "rows": [self.y - config.MAGNET_LENGTH + 1, self.y]
        }]
