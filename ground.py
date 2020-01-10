import config


class Ground:
    height = config.GROUND_HEIGHT

    def __init__(self):
        pass

    def draw(self):
        return [{
            "rows": [config.FRAME_HEIGHT - self.height + 1, config.FRAME_HEIGHT - 1],
            "cols": [0, config.FRAME_WIDTH-1],
            "objCode": config.GRID_CONSTS["ground"]
        }]

    def update(self):
        pass
