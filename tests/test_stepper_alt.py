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
        bus = SMBus(1)
        i2c_address = 0x0E

        stepper = Stepper(bus, i2c_address)
        stepper.init_limit_switch_forward()
        stepper.init_limit_switch_reverse()

        # Test limit switches
        switch = bus.read_byte_data(i2c_address, 0x01)
        print(f"Limit switch: {switch}")
        stepper.go_home_forward()
        sleep(10)
        switch = bus.read_byte_data(i2c_address, 0x01)
        print(f"Limit switch: {switch}")

#        stepper.go_home_reverse()
#        sleep(10)
#
#        # Test setting angles
#        angles = [-45, -90, -135, -180]
#        for angle in angles:
#            stepper.set_target_position(int(angle / STEPPER_DEG_PER_32_STEP))
#            sleep(5)
#
        # Disable stepper
        stepper.go_home_forward()
        sleep(10)
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.go_home_forward()
        stepper.de_energize()


if __name__ == "__main__":
    main()
