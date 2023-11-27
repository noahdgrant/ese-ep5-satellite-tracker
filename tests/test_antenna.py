#!/bin/python3

# Testing mainline for Antenna class

import sys
sys.path.append("..")

from src.antenna import Antenna
from time import sleep


def main():
    try:
        antenna = Antenna()

        # Test homing antenna
        antenna.go_home()

        # Test setting angles
#        angles = [0, -45, -90, -135, -180]
#        for angle in angles:
#            sleep(5)
#            antenna.set_alt_angle(angle)

        # Test shutdown sequence
        antenna.shutdown()

    except KeyboardInterrupt:
        antenna.shutdown()


if __name__ == "__main__":
    main()
