#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from time import sleep
from src.magnetometer import Magnetometer


def main():
    try:
        magnetometer = Magnetometer()

        print("Displaying readings from magnetometer")
        while True:
            reading = magnetometer.get_heading()
            print("Heading: {:.f} degrees".format(reading))
            sleep(1)

    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
