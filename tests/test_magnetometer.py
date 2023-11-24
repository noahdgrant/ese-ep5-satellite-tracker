#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from smbus2 import SMBus
from src.magnetometer import Magnetometer
from time import sleep


def main():
    try:
        bus = SMBus(1)
        i2c_address = 0x1E
        magnetometer = Magnetometer(bus, i2c_address)

        print("Displaying readings from magnetometer")

        # Test loop
        while True:
            reading = magnetometer.read_mag()
            print("magnometer is reading: ", reading)
            sleep(1)

        print("Loop finished...")

    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
