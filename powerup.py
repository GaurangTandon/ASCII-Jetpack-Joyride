"""
Dragon powerup and the boss laser implemented
"""

from colorama import Fore
import config
from generic import GenericFrameObject
from player import Laser


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
    stringRepr = [
        "-  -          ------              ",
        " -  -        -  --  -        -----",
        "  -  -      -  -  -  -      - .. =",
        "   -  -    -  -    -  -    -  -=  ",
        "    -  -  -  -      -  -  -  -    ",
        "     -  --  -        -  --  -     ",
        "      ------          ------      "
    ]

    color = [Fore.WHITE, None]
    MAX_BULLETS = 20
    TYPE = "playerdragon"

    def __init__(self, game):
        super().__init__()
        self.y = config.FRAME_HEIGHT / 2
        self.x = 15
        self.lifes = 3
        self.current_bullets = 0
        self.game_obj = game

    def wiggle(self):
        pass

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
        if self.current_bullets + 3 >= self.MAX_BULLETS:
            return []

        right_point = self.x + self.width
        l1 = Laser(right_point, self._get_middle(), self.game_obj)
        l2 = Laser(right_point, self.y, self.game_obj)
        l3 = Laser(right_point, self.y - self.height + 1, self.game_obj)
        self.current_bullets += 3

        return [l1, l2, l3]

    def _check_bounds(self):
        self.y = max(self.y, self.height - 1)
        self.y = min(self.y, config.FRAME_BOTTOM_BOUNDARY)

        for obj in self.game_obj.rendered_objects:
            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            to_delete = False

            if obj.TYPE == "coin":
                for point in common_points:
                    # TODO: play sound
                    pass
                to_delete = True
            elif obj.TYPE in ["firebeam", "bosslaser"]:
                self.lifes -= 1
                to_delete = True

            if to_delete:
                self.game_obj.delete_id_list.append(obj.id)
