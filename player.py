"""
Module for the player and his/her laser
"""

# requires module gi which is present in py3.6 but not in py3.7
# no idea why :/ gotta setup virtual env i guess -_-
# from playsound import playsound
import time
from math import sqrt
from colorama import Fore, Back
from util import tiler
import config
from generic import GenericFrameObject
from obstacle import Magnet


PLAYER_COLOR = Fore.WHITE


class Player(GenericFrameObject):
    """
    Our hero
    """
    startYCoord = config.FRAME_HEIGHT - config.GROUND_HEIGHT - 1
    # maintain rectangular shapes for ease of collision detection
    stringRepr = [
        "|/\\|",
        "|\\/|",
        "-||-",
        " || ",
        "----",
        "||||",
    ]

    color = [PLAYER_COLOR, None]

    DRAG_CONSTANT = 0.1
    X_IMPULSE = 1
    Y_IMPULSE = 1
    TYPE = "player"
    MAX_BULLETS = 10
    last_used_shield = -1
    SHIELD_TIME = 10
    SHIELD_REGEN_TIME = 60

    def __init__(self, obj_game):
        super().__init__()

        # x and y coordinate of the player's leftmost bottommost point
        self.x = config.FRAME_LEFT_BOUNDARY
        self.y = self.startYCoord

        # number of frames for which the player is touching the ceiling
        self.was_touching_ceiling = 0

        self.y_vel = 0
        self.x_vel = 0
        self.game_obj = obj_game

        self.y_acc = 0
        self.x_acc = 0

        self.current_bullets = 0
        self.w_key = False

        self.lifes = 3
        self.shield_activated = False

    def get_remaining_shield_time(self):
        """
        Calculate how much time left until next shield is available
        """
        curr = time.time()

        diff = curr - self.last_used_shield
        diff = self.SHIELD_REGEN_TIME + self.SHIELD_TIME - diff
        return max(0, diff)

    def activate_shield(self):
        """
        Activates player shield if it is available
        """
        if self.get_remaining_shield_time() == 0:
            self.shield_activated = True
            self.last_used_shield = time.time()

    def _get_middle(self):
        return self.y - self.height / 2

    def _get_top(self):
        return self.y - self.height + 1

    def update(self, last_key_pressed):
        """
        Called by Game to update the player stuff
        """
        magnet_x, magnet_y = self.game_obj.get_magnet_coords()

        if magnet_x is not None:
            x_dist = magnet_x - self.x
            y_dist = (magnet_y - self.y)*2
            hyp = sqrt(x_dist * x_dist + y_dist * y_dist)

            if hyp != 0:
                self.x_acc = (x_dist / hyp) * Magnet.FORCE_CONSTANT
                self.y_acc = (y_dist / hyp) * Magnet.FORCE_CONSTANT
            else:
                self.x_acc = 0
                self.y_acc = 0
        else:
            self.x_acc = 0
            self.y_acc = 0

        if self.shield_activated and time.time() - self.last_used_shield >= self.SHIELD_TIME:
            self.shield_activated = False

        color_val = Fore.BLUE if self.shield_activated else PLAYER_COLOR

        self.__class__.stringRepr[-1] = "||||"
        self.__class__.color = tiler(
            [color_val, None], self.height, self.width)

        # keypress gives an impulse, not an accn
        if last_key_pressed == 'w':
            self.y_vel -= self.Y_IMPULSE
        elif last_key_pressed == 's':
            self.y_vel += self.Y_IMPULSE
        elif last_key_pressed == 'a':
            self.x_vel -= self.X_IMPULSE * config.X_VEL_FACTOR
            self.__class__.stringRepr[-1] = "////"
        elif last_key_pressed == 'd':
            self.x_vel += self.X_IMPULSE * config.X_VEL_FACTOR
            self.__class__.stringRepr[-1] = "\\\\\\\\"

        if str(last_key_pressed) in 'sw':
            self.__class__.color[-1] = tiler([color_val,
                                              Back.MAGENTA], 1, self.width)

        self._generate_draw_obj()
        self.y_vel += config.GRAVITY_ACC
        self.y_vel += self.y_acc
        self.x_vel += self.x_acc
        drag_value = min(self.DRAG_CONSTANT * self.x_vel *
                         self.x_vel, abs(1))
        self.x_vel += (-1 if self.x_vel > 0 else 1) * drag_value

        self.x += round(self.x_vel)
        self.y += round(self.y_vel)
        self.x = min(self.x, 2 * config.FRAME_SPAWN_OFFSET +
                     config.FRAME_RIGHT_BOUNARY)

        self._check_bounds()

    def fire_laser(self):
        """
        Called by Game when user presses Space
        """
        if self.current_bullets >= self.MAX_BULLETS:
            return []

        laser = Laser(self.x, self._get_middle(), self.game_obj)
        self.current_bullets += 1

        return [laser]

    def _check_bounds(self):
        touched_ceil = self.y <= self.height - 1
        touched_bottom = self.y >= self.startYCoord

        self.y = max(self.y, self.height - 1)
        self.y = min(self.y, self.startYCoord)

        # low value makes it very awkward
        remain_at_the_top_threshold = 10
        # without this jetpack gets stuck at the top
        if touched_ceil and self.was_touching_ceiling >= remain_at_the_top_threshold:
            # do not add a fractional quantity
            self.y += 1

        # can't move anymore
        if touched_bottom or touched_ceil:
            self.y_vel = 0
            self.y_acc = 0
            self.was_touching_ceiling += int(touched_ceil)
        else:
            self.was_touching_ceiling = 0

        if self.x >= config.FRAME_RIGHT_BOUNARY:
            self.x = config.FRAME_RIGHT_BOUNARY
            self.x_vel = 0

        if self.x <= config.FRAME_LEFT_BOUNDARY:
            self.x = config.FRAME_LEFT_BOUNDARY
            self.x_vel = 0

        player_hit = False
        for obj in self.game_obj.get_rendered_objects():
            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            to_delete = False

            if obj.TYPE == "coin":
                for _ in common_points:
                    self.game_obj.increment_score()
                to_delete = True
            elif obj.TYPE in ["firebeam", "bosslaser"]:
                if not self.shield_activated:
                    player_hit = True
                    to_delete = True
            elif obj.TYPE == "speed":
                self.game_obj.speed_powerup()
                self.game_obj.set_speed_on_time(time.time())
                to_delete = True

            if to_delete:
                self.game_obj.append_to_delete_list(obj.id)

        if player_hit:
            self.lifes -= 1

    def decrement_bullets(self):
        """
        setter
        """
        self.current_bullets -= 1

    def get_lives(self):
        """
        getter
        """
        return self.lifes

    def decrease_lives(self):
        """
        setter
        """
        self.lifes -= 1

    def get_shield_activated(self):
        """
        getter
        """
        return self.shield_activated

    def get_last_used_shield(self):
        """
        getter
        """
        return self.last_used_shield


class Laser(GenericFrameObject):
    """
    Laser fired by our hero
    """
    stringRepr = [
        r"      ==\\",
        r"      ==//"
    ]
    color = [Fore.RED, None]
    TYPE = "laser"
    BOSS_DAMAGE_PLAYER = 10
    BOSS_DAMAGE_DRAGON = 5

    def __init__(self, x, y, game_obj):
        super().__init__()
        self.x = round(x)
        self.y = round(y)
        self.game_obj = game_obj

    def update(self):
        """
        Override of the generic update function
        """
        self.x += config.LASER_VEL * config.X_VEL_FACTOR

        if self.exceeds_bounds():
            self.game_obj.decrement_player_bullets()
            return GenericFrameObject.DEAD_FLAG

        # bullet can only delete one object
        delete_self = False

        for obj in self.game_obj.get_rendered_objects():
            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            if obj.TYPE == "boss":
                is_player = self.game_obj.get_player_type() == "player"
                self.game_obj.decrement_boss_health(
                    self.BOSS_DAMAGE_PLAYER if is_player else self.BOSS_DAMAGE_DRAGON)

                delete_self = True
                break

            if obj.TYPE in ["bosslaser", "firebeam"]:
                self.game_obj.append_to_delete_list(obj.id)
                # you get points for destroying opposition too
                self.game_obj.increment_score()
                delete_self = True
                break

        if delete_self:
            self.game_obj.decrement_player_bullets()
            return GenericFrameObject.DEAD_FLAG

        return None
