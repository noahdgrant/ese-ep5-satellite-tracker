#!/bin/python3

# Altitude stepper testing

import sys
sys.path.append("..")

from smbus2 import SMBus
from time import sleep
from src.stepper import Stepper

# I2C read offset addresses
MISC_FLAGS = 0x01

# I2C read bit codes
HOMING_ACTIVE = 0x10


def main():
    try:
        # Initialize stepper
        bus = SMBus(11)
        i2c_address = 0x0E

        stepper = Stepper(bus, i2c_address)
        stepper.max_angle = 180
        stepper.init_limit_switch_forward()
        stepper.init_limit_switch_reverse()

        # Testing forward home position
        print("going to forward home")
        stepper.go_home_forward()
        while (stepper.get_variable(0x01, 1)[0] & 0x10) != 0:
            print("wating to reach forward home")
            sleep(1)
        print("Forward home position: %s", stepper.get_current_position())

        # Testing finding maximum altitude steps
        stepper.set_target_velocity(-3200000)
        print("going reverse")
        while (stepper.get_variable(0x01, 1)[0] & 0x8) == 0:
            print("waiting reverse")
            sleep(1)
        stepper.max_position = stepper.get_current_position()
        print(f"Pos: {stepper.max_position}")

        # Test setting angles
        angles = [-45, -90, -135, -180]
        for angle in angles:
            stepper.set_target_angle(angle)
            sleep(5)
            print("Current position: %s", stepper.get_current_position())

        # Shutdown stepper
        stepper.go_home_forward()
        while (stepper.get_variable(MISC_FLAGS, 1)[0] & HOMING_ACTIVE) != 0:
            sleep(1)
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.go_home_forward()
        while (stepper.get_variable(MISC_FLAGS, 1)[0] & HOMING_ACTIVE) != 0:
            sleep(1)
        stepper.de_energize()


if __name__ == "__main__":
    main()
