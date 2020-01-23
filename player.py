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


PLAYER_COLOR =  Fore.YELLOW


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
        self._x = config.FRAME_LEFT_BOUNDARY
        self._y = self.startYCoord

        # number of frames for which the player is touching the ceiling
        self.__was_touching_ceiling = 0

        self.__y_vel = 0
        self.__x_vel = 0
        self.__game_obj = obj_game

        self.__y_acc = 0
        self.__x_acc = 0

        self.__current_bullets = 0

        self.__lifes = 3
        self.__shield_activated = False

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
            self.__shield_activated = True
            self.last_used_shield = time.time()

    def _get_middle(self):
        return self._y - self._height / 2

    def _get_top(self):
        return self._y - self._height + 1

    def update(self, last_key_pressed):
        """
        Called by Game to update the player stuff
        """
        magnet_x, magnet_y = self.__game_obj.get_magnet_coords()

        if magnet_x is not None:
            x_dist = magnet_x - self._x
            y_dist = (magnet_y - self._y)*2
            hyp = sqrt(x_dist * x_dist + y_dist * y_dist)

            if hyp != 0:
                self.__x_acc = (x_dist / hyp) * Magnet.FORCE_CONSTANT
                self.__y_acc = (y_dist / hyp) * Magnet.FORCE_CONSTANT
            else:
                self.__x_acc = 0
                self.__y_acc = 0
        else:
            self.__x_acc = 0
            self.__y_acc = 0

        if self.__shield_activated and time.time() - self.last_used_shield >= self.SHIELD_TIME:
            self.__shield_activated = False

        color_val = Fore.BLUE if self.__shield_activated else PLAYER_COLOR

        self.__class__.stringRepr[-1] = "||||"
        self.__class__.color = tiler(
            [color_val, None], self._height, self._width)

        # keypress gives an impulse, not an accn
        if last_key_pressed == 'w':
            self.__y_vel -= self.Y_IMPULSE
        elif last_key_pressed == 's':
            self.__y_vel += self.Y_IMPULSE
        elif last_key_pressed == 'a':
            self.__x_vel -= self.X_IMPULSE * config.X_VEL_FACTOR
            self.__class__.stringRepr[-1] = "////"
        elif last_key_pressed == 'd':
            self.__x_vel += self.X_IMPULSE * config.X_VEL_FACTOR
            self.__class__.stringRepr[-1] = "\\\\\\\\"

        if str(last_key_pressed) in 'sw':
            self.__class__.color[-1] = tiler([color_val,
                                              Back.MAGENTA], 1, self._width)

        self._generate_draw_obj()
        self.__y_vel += config.GRAVITY_ACC
        self.__y_vel += self.__y_acc
        self.__x_vel += self.__x_acc
        drag_value = min(self.DRAG_CONSTANT * self.__x_vel *
                         self.__x_vel, abs(1))
        self.__x_vel += (-1 if self.__x_vel > 0 else 1) * drag_value

        self._x += round(self.__x_vel)
        self._y += round(self.__y_vel)
        self._x = min(self._x, 2 * config.FRAME_SPAWN_OFFSET +
                      config.FRAME_RIGHT_BOUNARY)

        self._check_bounds()

    def fire_laser(self):
        """
        Called by Game when user presses Space
        """
        if self.__current_bullets >= self.MAX_BULLETS:
            return []

        laser = Laser(self._x, self._get_middle(), self.__game_obj)
        self.__current_bullets += 1

        return [laser]

    def _check_bounds(self):
        touched_ceil = self._y <= self._height - 1
        touched_bottom = self._y >= self.startYCoord

        self._y = max(self._y, self._height - 1)
        self._y = min(self._y, self.startYCoord)

        # low value makes it very awkward
        remain_at_the_top_threshold = 10
        # without this jetpack gets stuck at the top
        if touched_ceil and self.__was_touching_ceiling >= remain_at_the_top_threshold:
            # do not add a fractional quantity
            self._y += 1

        # can't move anymore
        if touched_bottom or touched_ceil:
            self.__y_vel = 0
            self.__y_acc = 0
            self.__was_touching_ceiling += int(touched_ceil)
        else:
            self.__was_touching_ceiling = 0

        if self._x >= config.FRAME_RIGHT_BOUNARY:
            self._x = config.FRAME_RIGHT_BOUNARY
            self.__x_vel = 0

        if self._x <= config.FRAME_LEFT_BOUNDARY:
            self._x = config.FRAME_LEFT_BOUNDARY
            self.__x_vel = 0

        player_hit = False
        for obj in self.__game_obj.get_rendered_objects():
            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            to_delete = False

            if obj.TYPE == "coin":
                for _ in common_points:
                    self.__game_obj.increment_score()
                to_delete = True
            elif obj.TYPE in ["firebeam", "bosslaser"]:
                if not self.__shield_activated:
                    player_hit = True
                    to_delete = True
            elif obj.TYPE == "speed":
                self.__game_obj.speed_powerup()
                self.__game_obj.set_speed_on_time(time.time())
                to_delete = True

            if to_delete:
                self.__game_obj.append_to_delete_list(obj.get_id())

        if player_hit:
            self.__lifes -= 1

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

    def get_shield_activated(self):
        """
        getter
        """
        return self.__shield_activated

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
    BOSS_DAMAGE = 5
    OBSTACLE_HIT_SCORE = 5

    def __init__(self, x, y, game_obj):
        super().__init__()
        self._x = round(x)
        self._y = round(y)
        self.__game_obj = game_obj

    def update(self):
        """
        Override of the generic update function
        """
        self._x += config.LASER_VEL * config.X_VEL_FACTOR

        if self.exceeds_bounds():
            self.__game_obj.decrement_player_bullets()
            return GenericFrameObject.DEAD_FLAG

        if self._x + self._width >= config.FRAME_RIGHT_BOUNARY:
            self.__game_obj.decrement_player_bullets()
            return GenericFrameObject.DEAD_FLAG

        # bullet can only delete one object
        delete_self = False

        for obj in self.__game_obj.get_rendered_objects():
            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            if obj.TYPE == "boss":
                is_player = self.__game_obj.get_player_type() == "player"
                self.__game_obj.decrement_boss_health(self.BOSS_DAMAGE)

                delete_self = True
                break

            if obj.TYPE in ["bosslaser", "firebeam"]:
                self.__game_obj.append_to_delete_list(obj.get_id())
                # you get points for destroying opposition too
                self.__game_obj.increment_score(self.OBSTACLE_HIT_SCORE)
                delete_self = True
                break

        if delete_self:
            self.__game_obj.decrement_player_bullets()
            return GenericFrameObject.DEAD_FLAG

        return None
