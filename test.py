# import subprocess
import sys
import select
import tty
import termios
import os
import numpy as np
from time import sleep

forward_list = ''
backward_list = ''

for i in range(30):
    for j in range(180):
        forward_list = forward_list + '/'
        backward_list = backward_list + '\\'
    forward_list = forward_list + '\n'
    backward_list = backward_list + '\n'


# why does one of the lines not work?
def main():
    print("\033[2J")  # clear
    # assert len(forward_list) == len(backward_list)
    while True:
        print(forward_list)
        sleep(0.5)
        print("\033[0;0H")
        print(backward_list)
        sleep(0.5)
        print("\033[0;0H")


if __name__ == "__main__":
    main()
