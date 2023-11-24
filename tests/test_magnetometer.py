#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from smbus2 import SMBus
from time import sleep
from src.magnetometer import Magnetometer


def main():
    try:
        bus = SMBus(11)
        i2c_address = 0x1E
        magnetometer = Magnetometer(bus, i2c_address)

        print("Displaying readings from magnetometer")
        while True:
            reading = magnetometer.get_reading()
            print(reading)
            sleep(1)

    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
