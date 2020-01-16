import signal
from game import Game

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    Game()
