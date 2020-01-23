"""
Dragon powerup and the boss laser implemented
"""

from colorama import Fore
import config
from generic import GenericFrameObject
from player import Laser

FRAMES = [
    [
        "              ________                               ",
        "             -    -   -           __)',-._     _     ",
        "_____       -    - -    -        ----    () '---(,', ",
        "-    -     -    -   -    -      - - -`  `'  .--_____/",
        " -    -   -    -     -    -    -   --. // .__..--,_/ ",
        "  -    - -    -       -    -  -    -                 ",
        "   -    -    -         -    --    -                  ",
        "    ^^^^^^^^^           ^^^^^^^^^^                   "
    ],
    [
        "             ________             __)',-._     _     ",
        "            -    -   -           ----    () '---(,', ",
        "____       -    - -    -        - - -`  `'  .--_____/",
        "    -     -    -   -    -      -   --. // .__..--,_/ ",
        "-    -   -    -     -    -    -    -                 ",
        " -    - -    -       -    -  -    -                  ",
        "  -    -    -         -    --    -                   ",
        "   ^^^^^^^^^           ^^^^^^^^^^                    "
    ],
    [
        "              ________                               ",
        "             -    -   -           __)',-._     _     ",
        "_____       -    - -    -        ----    () '---(,', ",
        "-    -     -    -   -    -      - - -`  `'  .--_____/",
        " -    -   -    -     -    -    -   --. // .__..--,_/ ",
        "  -    - -    -       -    -  -    -                 ",
        "   -    -    -         -    --    -                  ",
        "    ^^^^^^^^^           ^^^^^^^^^^                   "
    ],
    [
        "               ________                              ",
        "_____         -    -   -                             ",
        "-    -       -    - -    -        __)',-._     _     ",
        " -    -     -    -   -    -      ----    () '---(,', ",
        "  -    -   -    -     -    -    - - -`  `'  .--_____/",
        "   -    - -    -       -    -  -   --. // .__..--,_/ ",
        "    -    -    -         -    --    -                 ",
        "     ^^^^^^^^^           ^^^^^^^^^^                  "
    ],
    [
        "_____          _________                             ",
        "-    -         -    -   -                            ",
        " -    -       -    - -    -                          ",
        "  -    -     -    -   -    -      __)',-._     _     ",
        "   -    -   -    -     -    -    ----    () '---(,', ",
        "    -    - -    -       -    -  - - -`  `'  .--_____/",
        "     -    -    -         -    --   --. // .__..--,_/ ",
        "      ^^^^^^^^^           ^^^^^^^^^^                 "
    ],
]


class DragonPowerup(GenericFrameObject):
    """
    Dragon powerup
    - more bullets per shot
    - lesser damage per bullet
    - also wiggles
    - same number of lives
    - moves slowly, easier target for boss bullets
    - bullets follow the dragon with 100% accuracy
    """

    MAX_BULLETS = 6
    TYPE = "playerdragon"

    def __init__(self, game):
        self.frame = 0
        self.count = 0
        self.__class__.stringRepr = FRAMES[0]
        self.__class__.color = [Fore.WHITE, None]
        super().__init__()
        self.y = config.FRAME_HEIGHT / 2
        self.x = 5 + config.FRAME_LEFT_BOUNDARY
        self.__lifes = 1
        self.__current_bullets = 0
        self.__game_obj = game

    def wiggle(self):
        """
        Changes frame of the dragon every 5 frames
        """
        if self.count % 5 == 0:
            self.__class__.stringRepr = FRAMES[self.frame]
            self.__class__.color = [Fore.WHITE, None]
            self._generate_draw_obj()
            self.frame += 1
            self.frame %= len(FRAMES)
        self.count += 1

    def update(self, last_key_pressed):
        """
            Boss has no velocity, not affected by gravity
            Boss is not affected by magnet
        """

        # keypress gives an impulse, not an accn
        if last_key_pressed == 'w':
            self.y -= 1
        elif last_key_pressed == 's':
            self.y += 1

        self.wiggle()
        self._check_bounds()

    def _get_middle(self):
        return self.y - self.height / 2

    def fire_laser(self):
        """
        Called by Game when user presses Space
        """
        res = []

        right_point = self.x + self.width
        if self.__current_bullets >= self.MAX_BULLETS:
            return res

        laser1 = Laser(right_point, self._get_middle(), self.__game_obj)
        res.append(laser1)
        self.__current_bullets += 1
        if self.__current_bullets >= self.MAX_BULLETS:
            return res

        laser2 = Laser(right_point, self.y, self.__game_obj)
        res.append(laser2)
        self.__current_bullets += 1
        if self.__current_bullets >= self.MAX_BULLETS:
            return res

        laser3 = Laser(right_point, self.y - self.height + 1, self.__game_obj)
        res.append(laser3)
        self.__current_bullets += 1

        return res

    def _check_bounds(self):
        self.y = max(self.y, self.height - 1)
        self.y = min(self.y, config.FRAME_BOTTOM_BOUNDARY)

        for obj in self.__game_obj.get_rendered_objects():
            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            to_delete = False

            if obj.TYPE == "coin":
                self.__game_obj.inc_score(len(common_points))
                to_delete = True
            elif obj.TYPE in ["firebeam", "bosslaser"]:
                self.__lifes -= 1
                to_delete = True

            if to_delete:
                self.__game_obj.append_to_delete_list(obj.id)

    def decrement_bullets(self):
        """
        setter
        """
        self.__current_bullets -= 1

    def get_lives(self):
        """
        getter
        """
        return self.__lifes

    def decrease_lives(self):
        """
        setter
        """
        self.__lifes -= 1
