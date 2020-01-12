from colorama import Fore
import config
from generic import GenericFrameObject


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

    def __init__(self, obj_game):
        super().__init__()

        # x and y coordinate of the player's leftmost bottommost point
        self.x = config.FRAME_LEFT_BOUNDARY
        self.y = self.startYCoord

        self.y_vel = 0
        self.x_vel = 0
        self.game_obj = obj_game

        self.y_acc = 0

        self.lifes = 3
        self.health = 100

    def get_top(self):
        return self.y - self.height + 1

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        self.y_vel += config.GRAVITY_ACC
        self.y_vel += self.y_acc

        # self.x = round(self.x)
        # self.y = round(self.y)

        self.check_bounds()

    def reset_no_key(self):
        self.x_vel = 0

    def fire_laser(self):
        laser = Laser()

        laser.x = self.x
        laser.y = self.y

        return laser

    def update_key(self, key):
        if key not in 'ad':
            self.x_vel = 0

        if key != 'w':
            self.y_acc = 0

        if key == 'a':
            self.x_vel = -1
        elif key == 'd':
            self.x_vel = 1
        elif key == 'w':
            # TODO: why do I need this initial push?
            if self.y_acc == 0:
                self.y_vel -= 0.001

            # TODO: gotta fix this, feels janky
            self.y_acc = -0.12
        elif key == ' ':
            return self.fire_laser()
        else:
            assert False

        return None

    def check_bounds(self):
        # check sky bound
        self.y = max(self.y, self.height - 1)

        # check ground bound
        self.y = min(self.y, self.startYCoord)

        # can't move anymore
        if self.y >= self.startYCoord or self.y <= self.height - 1:
            self.y_vel = 0
            self.y_acc = 0

        # hack to not make the jetpack get stuck at the top
        if self.y <= self.height - 1:
            self.y += 0.01

        # TODO: the window should also move accordingly to accommodate
        if self.x >= config.FRAME_RIGHT_BOUNARY:
            self.x = config.FRAME_RIGHT_BOUNARY
            self.x_vel = 0

        if self.x <= config.FRAME_LEFT_BOUNDARY:
            self.x = config.FRAME_LEFT_BOUNDARY
            self.x_vel = 0

        for obj in self.game_obj.rendered_objects:
            pass
            # check collision
            # if self.collide(obj):
            #     if obj.isCoin:
            #         pass
            #     else:
            #         pass

        if self.lifes == 0:
            self.dead()


class Laser(GenericFrameObject):
    stringRepr = ["==>"]

    def update(self):
        self.x += config.LASER_VEL

        if self.exceeds_bounds():
            return GenericFrameObject.DEAD_FLAG
