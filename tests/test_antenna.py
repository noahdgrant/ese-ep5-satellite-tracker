#!/bin/python3

# Testing mainline for Antenna class

from time import sleep

import sys
sys.path.append("..")

from src.antenna import Antenna


def main():
    try:
        antenna = Antenna()

        # Test homing antenna
        antenna.go_home()

        # Test setting altitude angles
        angles = [-45]
        for angle in angles:
            sleep(5)
            antenna.set_alt_angle(angle)

        # Test setting azimuth angles
        angles = [270, 180, 45]
        for angle in angles:
            sleep(8)
            antenna.set_azi_angle(angle)

        sleep(30)

        # Test shutdown sequence
        antenna.shutdown()

    except KeyboardInterrupt:
        antenna.shutdown()


if __name__ == "__main__":
    main()
