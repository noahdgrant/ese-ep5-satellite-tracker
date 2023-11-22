#!/bin/python3

# Altitude stepper testing

import sys
sys.path.append("..")

from smbus2 import SMBus
from time import sleep
from src.stepper import Stepper

STEPPER_DEG_PER_FULL_STEP = 1.8
STEPPER_DEG_PER_32_STEP = STEPPER_DEG_PER_FULL_STEP / 32


def main():
    try:
        # Initialize stepper
        bus = SMBus(11)
        i2c_address = 0x0f

        stepper = Stepper(bus, i2c_address)
        
        stepper.set_target_velocity(-3200000)
        sleep(5)
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.go_home_forward()
        stepper.de_energize()


if __name__ == "__main__":
    main()