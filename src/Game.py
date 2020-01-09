import signal
import Player from "player.py"


class Game():
    FRAME_RATE = 10
    player = None
    _refresh_time = 1 / FRAME_RATE

    def __init__(self):
        self.loop()
        player = Player()
        signal.signal(signal.SIGALRM, loop)

    def draw(self):
        player.draw()

    def loop(self):
        self.draw()
        signal.setitimer(signal.ITIMER_REAL, _refresh_time)
