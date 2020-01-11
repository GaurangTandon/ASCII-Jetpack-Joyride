import config
from generic import GenericFrameObject
from colorama import Fore, Back


class Boss(GenericFrameObject):
    X_THRESHOLD = 15
    Y_VEL = 0.1
    START_Y = config.FRAME_HEIGHT / 2

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
        self.__class__.stringRepr = [[c for c in x]
                                     for x in self.__class__.stringRepr]
        super().__init__()
        self.yVel = 0

        self.y = self.START_Y
        self.x = config.FRAME_SPAWN_X

        self.gameObj = gameObj

    def update(self):
        self.y += self.yVel

        # get the player's coordinates and move towards it
        if self.gameObj.player.y < self.y:
            self.yVel = -self.Y_VEL
        else:
            self.yVel = self.Y_VEL
