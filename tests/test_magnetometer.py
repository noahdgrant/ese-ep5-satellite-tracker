#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from smbus2 import SMBus
from src.magnetometer import Magnetometer


def main():
    bus = SMBus(1)
    i2c_address = 0x1E
    magnetometer = Magnetometer(bus, i2c_address)

    if input("Do you want to calibrate the magnetometer? [y/n] ") == "y":
        magnetometer.calibrate()

    while True:
        print("Heading: {:.2f} degrees".format(magnetometer.get_heading()))


if __name__ == "__main__":
    main()
