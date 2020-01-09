import config


class Ground:
    def __init__(self):
        self.height = config.GROUND_HEIGHT

    def draw(self):
        return {
            "from_row": config.FRAME_HEIGHT - config.GROUND_HEIGHT - 1,
            "to_row": config.FRAME_HEIGHT - 1,
            "from_col": 0,
            "to_col": config.FRAME_WIDTH-1,
            "objCode": config.GRID_CONSTS["ground"]
        }

    def update(self):
        pass
