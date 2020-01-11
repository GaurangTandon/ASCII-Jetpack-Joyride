# TODO: should be based on terminal height
FRAME_WIDTH = 150
FRAME_HEIGHT = 50
FRAME_X_VELOCITY = 10
FRAME_RATE = 10
FRAME_LEFT_BOUNDARY = 10
# enemies can spawn in this region
FRAME_RIGHT_BOUNARY = FRAME_WIDTH - 40
FRAME_SPAWN_OFFSET = 20

GROUND_HEIGHT = 2

GRAVITY_ACC = 0.1

BOSS_X_THRESHOLD = 100

LASER_VEL = 2

COIN_VALUE = 1

FIREBEAM_LENGTH = 5


GRID_CONSTS = {
    "player": 1,
    "background": 2,
    "ground": 3,
    "coin": 4,
    "magnet": 5,
    "firebeam": 6,
    "playerlaser": 7
}
