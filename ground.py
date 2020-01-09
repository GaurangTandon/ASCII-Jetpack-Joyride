import config


class Ground:
    def __init__(self):
        self.height = config.GROUND_HEIGHT

    def draw(self, grid):
        for row in range(config.FRAME_HEIGHT - 1, config.FRAME_HEIGHT - config.GROUND_HEIGHT - 1, -1):
            for cell in range(0, config.FRAME_WIDTH):
                grid[row][cell] = config.GRID_CONSTS["ground"]
