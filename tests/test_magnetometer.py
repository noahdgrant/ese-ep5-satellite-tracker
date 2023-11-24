#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

import board
from src.magnetometer import Magnetometer


def main():
    try:
        bus = board.I2C()
        i2c_address = 0x1E
        magnetometer = Magnetometer(bus, i2c_address)

        print("Displaying readings from magnetometer")

        # Test loop
        while True:
            reading = magnetometer.get_heading()
            print("magnometer is reading: ", reading)

        print("Loop finished...")

    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
