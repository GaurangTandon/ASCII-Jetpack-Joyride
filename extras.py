from colorama import Fore
from generic import GenericFrameObject
import config


class BackgroundObject(GenericFrameObject):
    """
    Frame objects that stay in the background and move super slowly
    """

    def update(self):
        self.x += (3*config.FRAME_MOVE_SPEED)//4
        return super().update()


class Mountain(BackgroundObject):
    stringRepr = [
        r"                                       /\                                ",
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
        r"ooooooooooooooooooooooooooooooooooooooooooooooooooooooooo                "
    ]
    color = [Fore.WHITE, None]
    TYPE = "mountain"

    def __init__(self):
        super().__init__()

        self.x = config.FRAME_SPAWN_X - self.width
        self.y = config.FRAME_BOTTOM_BOUNDARY


class Cloud(BackgroundObject):
    stringRepr = [
        "                  .-~~~-.     ",
        "  .- ~ ~-(       )_         _ ",
        " /                     ~ -.   ",
        "|                           \\ ",
        " \                         .' ",
        "   ~- . _____________ . -~    "
    ]

    color = [Fore.WHITE, None]
    TYPE = "cloud"

    def __init__(self):
        super().__init__()
        self.x = config.FRAME_SPAWN_X - self.width
        self.y = self.height