import config
from generic import GenericFrameObject
from colorama import Fore, Back


class Boss(GenericFrameObject):
    # get something rectangular

    # create an aura around him, basically make him a rectangular box :P
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

    def __init__(self):
        self.__class__.stringRepr = [[c for c in x]
                                     for x in self.__class__.stringRepr]
        super().__init__()

    def update(self):
        # TODO: should move up and down and fire lasers
        pass
