#!/bin/python3

# Azimuth stepper testing

import sys
sys.path.append("..")

from smbus2 import SMBus
from time import sleep
from src.stepper import Stepper


def main():
    try:
        # Initialize stepper
        bus = SMBus(11)
        i2c_address = 0x0F

        stepper = Stepper(bus, i2c_address)

        stepper.set_target_velocity(-3200000)
        sleep(5)
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.de_energize()


if __name__ == "__main__":
    main()
