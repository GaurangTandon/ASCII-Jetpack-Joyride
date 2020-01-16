from math import sqrt
from colorama import Fore, Back
from util import tiler
import config
from generic import GenericFrameObject
from obstacle import Magnet


class Player(GenericFrameObject):
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

    color = [Fore.RED, None]

    DRAG_CONSTANT = 0.1
    X_IMPULSE = 1
    Y_IMPULSE = 1
    TYPE = "player"
    MAX_BULLETS = 10

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

    def _get_middle(self):
        return self.y - self.height / 2

    def get_top(self):
        return self.y - self.height + 1

    def update_overriden(self, last_key_pressed):
        if self.game_obj.magnet_obj:
            # TODO: messed up
            num = Magnet.FORCE_CONSTANT
            x_dist = self.game_obj.magnet_obj.x - self.x
            y_dist = self.game_obj.magnet_obj.y - self.y
            hyp = sqrt(x_dist * x_dist + y_dist * y_dist)

            if hyp != 0:
                force = num / (hyp * hyp)
                self.x_acc = (x_dist / hyp) * force
                self.y_acc = (y_dist / hyp) * force
            else:
                self.x_acc = 0
                self.y_acc = 0
        else:
            self.x_acc = 0
            self.y_acc = 0

        self.__class__.stringRepr[-1] = "||||"
        self.__class__.color[-1] = tiler([Fore.RED, None], 1, self.width)

        # keypress gives an impulse, not an accn
        if last_key_pressed == 'w':
            self.y_vel -= self.Y_IMPULSE
        elif last_key_pressed == 's':
            self.y_vel += self.Y_IMPULSE
        elif last_key_pressed == 'a':
            self.x_vel -= self.X_IMPULSE
            self.__class__.stringRepr[-1] = "////"
        elif last_key_pressed == 'd':
            self.x_vel += self.X_IMPULSE
            self.__class__.stringRepr[-1] = "\\\\\\\\"

        if str(last_key_pressed) in 'sw':
            self.__class__.color[-1] = tiler([Fore.RED,
                                              Back.MAGENTA], 1, self.width)

        self._generate_draw_obj()
        self.y_vel += config.GRAVITY_ACC
        self.y_vel += self.y_acc
        self.x_vel += self.x_acc
        drag_value = min(self.DRAG_CONSTANT * self.x_vel *
                         self.x_vel, abs(self.x_vel))
        self.x_vel += (-1 if self.x_vel > 0 else 1) * drag_value

        self.x += round(self.x_vel)
        self.y += round(self.y_vel)

        self.check_bounds()

    def fire_laser(self):
        if self.current_bullets >= self.MAX_BULLETS:
            return None

        laser = Laser(self.x, self._get_middle(), self.game_obj)
        self.current_bullets += 1

        return laser

    def check_bounds(self):
        touched_ceil = self.y <= self.height - 1
        touched_bottom = self.y >= self.startYCoord

        self.y = max(self.y, self.height - 1)
        self.y = min(self.y, self.startYCoord)

        remain_at_the_top_threshold = 20
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

        list_to_delete = []
        i = -1
        for obj in self.game_obj.rendered_objects:
            i += 1
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
                list_to_delete.append(i)

        list_to_delete.reverse()
        for j in list_to_delete:
            self.game_obj.rendered_objects.pop(j)


class Laser(GenericFrameObject):
    stringRepr = ["==>"]
    color = [Fore.RED, None]
    TYPE = "laser"
    BOSS_DAMAGE = 10

    def __init__(self, x, y, game_obj):
        super().__init__()
        self.x = round(x)
        self.y = round(y)
        self.game_obj = game_obj

    def update(self):
        self.x += config.LASER_VEL

        if self.exceeds_bounds():
            self.game_obj.player.current_bullets -= 1
            return GenericFrameObject.DEAD_FLAG

        # bullet can only delete one object
        to_delete = None
        i = -1
        delete_self = False

        for obj in self.game_obj.rendered_objects:
            i += 1

            common_points = self.check_collision(obj)
            if len(common_points) == 0:
                continue

            if obj.TYPE == "boss":
                self.game_obj.boss_obj.health -= self.BOSS_DAMAGE
                delete_self = True
                break

            if obj.TYPE in ["bosslaser", "firebeam"]:
                to_delete = i
                delete_self = True
                break

        if to_delete:
            # todo: this can lead to undefined behavior since
            # we are popping objects while looping over the list
            self.game_obj.rendered_objects.pop(to_delete)

        if delete_self:
            self.game_obj.player.current_bullets -= 1
            return GenericFrameObject.DEAD_FLAG

        return None
