#!/bin/python3

# Altitude stepper testing

from src.stepper import Stepper
from smbus2 import SMBus
from time import sleep

STEPPER_DEG_PER_FULL_STEP = 1.8
STEPPER_DEG_PER_32_STEP = STEPPER_DEG_PER_FULL_STEP / 32


def main():
    try:
        # Initialize stepper
        bus = SMBus(1)
        i2c_address = 14

        stepper = Stepper(bus, i2c_address)
        stepper.init_limit_switch_forward()
        stepper.init_limit_switch_reverse()

        # Test limit switches
        stepper.go_home_forward()
        sleep(2)

        stepper.go_home_reverse()
        sleep(2)

        # Test setting angle
        stepper.set_target_position(-45 / STEPPER_DEG_PER_32_STEP)
        sleep(2)

        stepper.set_target_position(-90 / STEPPER_DEG_PER_32_STEP)
        sleep(2)

        stepper.set_target_position(-135 / STEPPER_DEG_PER_32_STEP)
        sleep(2)

        stepper.set_target_position(-180 / STEPPER_DEG_PER_32_STEP)
        sleep(2)

        stepper.set_target_position(0 / STEPPER_DEG_PER_32_STEP)
        sleep(2)

        # Disable stepper
        stepper.go_home_forward()
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.go_home_forward()
        stepper.de_energize()


if __name__ == "__main__":
    main()
