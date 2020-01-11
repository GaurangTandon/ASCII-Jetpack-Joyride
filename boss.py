import time
import config
from generic import GenericFrameObject
from colorama import Fore, Back


class Boss(GenericFrameObject):
    X_THRESHOLD = 15
    Y_VEL = 0.1
    START_Y = config.FRAME_HEIGHT / 2
    FIRE_INTERVAL = 1

    # create an aura around him, basically make him a rectangular box to ease collision detection :P
    stringRepr = [
        "---------------",
        "|   /     \\   |",
        "|  ((     ))  |",
        "=   \\\\_v_//   =",
        "=====)_^_(=====",
        "====/ O O \\====",
        "== | /_ _\\ | ==",
        "|   \\/_ _\\/   |",
        "|    \\_ _/    |",
        "|    (o_o)    |",
        "|     VwV     |",
        "---------------"
    ]

    color = [Fore.WHITE, Back.RED]

    def __init__(self, gameObj):
        super().__init__()
        self.yVel = 0

        self.y = self.START_Y
        self.x = config.FRAME_SPAWN_X

        self.gameObj = gameObj

        self.health = 100
        self.lastFired = -1

    def fireGun(self):
        # TODO: fix velocity to be better directed to the player
        if self.gameObj.player.y < self.y:
            initvy = -1
        else:
            initvy = 1

        self.gameObj.renderedObjects.append(
            BossLaser(initvy, -1, self.x, self.y - self.height / 2))

        self.lastFired = time.time()

    def update(self):
        self.y += self.yVel

        # get the player's coordinates and move towards it
        if self.gameObj.player.y < self.y:
            self.yVel = -self.Y_VEL
        else:
            self.yVel = self.Y_VEL

        if time.time() - self.lastFired >= self.FIRE_INTERVAL:
            self.fireGun()


class BossLaser(GenericFrameObject):
    stringRepr = [
        "-^-",
        "<O>",
        "-v-"
    ]
    color = [Fore.BLACK, Back.BLACK]

    def __init__(self, initvy, initvx, initX, initY):
        super().__init__()

        self.y = initY
        self.x = initX
        self.velY = initvy
        self.velX = initvx

    def update(self):
        self.x += self.velX
        self.y += self.velY
