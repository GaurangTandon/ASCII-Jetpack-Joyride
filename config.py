"""
Constants related to the frame and the game
"""
from colorama import Back

GROUND_HEIGHT = 2

FRAME_WIDTH = 300
FRAME_HEIGHT = 40
FRAME_X_VELOCITY = 10
FRAME_RATE = 20
FRAME_LEFT_BOUNDARY = 110
# enemies can spawn in this region
FRAME_RIGHT_BOUNARY = FRAME_WIDTH - 40
FRAME_SPAWN_OFFSET = -20
# spawn some point outside the visible frame
FRAME_SPAWN_X = FRAME_RIGHT_BOUNARY
FRAME_BOTTOM_BOUNDARY = FRAME_HEIGHT - GROUND_HEIGHT - 1

FRAME_MOVE_SPEED = 2

GRAVITY_ACC = 0.15

LASER_VEL = 2

COIN_VALUE = 1

FIREBEAM_LENGTH = 5

DEBUG = False
BACK_COLOR = Back.BLACK

# for the speed up
X_VEL_FACTOR = 1
