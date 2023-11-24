#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from time import sleep
import board
from src.magnetometer import Magnetometer
from smbus2 import SMBus
import busio


def main():
    try:
        bus = board.I2C()
        i2c_address = 0x1E
        magnetometer = Magnetometer(bus, i2c_address)

        print("Displaying readings from magnetometer")
        while True:
            reading = magnetometer.get_heading()
            print(reading)
            sleep(1)

    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
