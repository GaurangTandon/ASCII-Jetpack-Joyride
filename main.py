from game import Game
import signal

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_IGN)
    Game()
