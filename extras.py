"""
The usual scenery around you
"""

from colorama import Fore
from generic import GenericFrameObject
import config


class BackgroundObject(GenericFrameObject):
    """
    Frame objects that stay in the background and move super slowly
    """

    def update(self):
        self._x += (3*config.FRAME_MOVE_SPEED)//4
        return super().update()


class Mountain(BackgroundObject):
    """
    A large mountain with a house in it that looks dope
    """
    stringRepr = [
        r"                                                                         ",
        r"                              /\  //\\                                   ",
        r"                       /\    //\\///\\\        /\                        ",
        r"                      //\\  ///\////\\\\  /\  //\\                       ",
        r"         /\          /  ^ \/^ ^/^  ^  ^ \/^ \/  ^ \                      ",
        r"        / ^\    /\  / ^   /  ^/ ^ ^ ^   ^\ ^/  ^^  \                     ",
        r"       /^   \  / ^\/ ^ ^   ^ / ^  ^    ^  \/ ^   ^  \       *            ",
        r"      /  ^ ^ \/^  ^\ ^ ^ ^   ^  ^   ^   ____  ^   ^  \     /|\           ",
        r"     / ^ ^  ^ \ ^  _\___________________|  |_____^ ^  \   /||o\          ",
        r"    / ^^  ^ ^ ^\  /______________________________\ ^ ^ \ /|o|||\         ",
        r"   /  ^  ^^ ^ ^  /________________________________\  ^  /|||||o|\        ",
        r"  /^ ^  ^ ^^  ^    ||___|___||||||||||||___|__|||      /||o||||||\       ",
        r" / ^   ^   ^    ^  ||___|___||||||||||||___|__|||          | |           ",
        r"/ ^ ^ ^  ^  ^  ^   ||||||||||||||||||||||||||||||oooooooooo| |ooooooo    ",
        r"ooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
    ]
    color = [Fore.WHITE, None]
    TYPE = "mountain"

    def __init__(self):
        super().__init__()

        self._x = config.FRAME_RIGHT_BOUNARY + self._width
        self._y = config.FRAME_BOTTOM_BOUNDARY


class Cloud(BackgroundObject):
    """
    Sweet cloud
    """
    stringRepr = [
        "                  .-~~~-.     ",
        "  .- ~ ~-(       )_         _ ",
        " /                     ~ -.   ",
        r"|                           \ ",
        r" \                         .' ",
        "   ~- . _____________ . -~    "
    ]

    color = [Fore.WHITE, None]
    TYPE = "cloud"

    def __init__(self):
        super().__init__()
        self._x = config.FRAME_RIGHT_BOUNARY + self._width
        self._y = self._height
