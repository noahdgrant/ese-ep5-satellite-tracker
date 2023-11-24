#!/bin/python3

# Altitude stepper testing

import sys
sys.path.append("..")

from smbus2 import SMBus
from time import sleep
from src.stepper import Stepper


def main():
    try:
        max_angle = 180
        max_position = 0

        # Initialize stepper
        bus = SMBus(11)
        i2c_address = 0x0E

        stepper = Stepper(bus, i2c_address)
        stepper.init_limit_switch_forward()
        stepper.init_limit_switch_reverse()

        # Testing forward home position
        print("going to forward home")
        stepper.go_home_forward()
        while (stepper.get_variable(stepper.MISC_FLAGS, 1)[0] &
               stepper.HOMING_ACTIVE) != 0:
            print("wating to reach forward home")
            sleep(1)
        print("Forward home position: %s", stepper.get_current_position())

        # Testing finding maximum altitude steps
        stepper.set_target_velocity(-3200000)
        print("going reverse")
        while (stepper.get_variable(stepper.MISC_FLAGS, 1)[0] &
               stepper.REVERSE_LIMIT_SWITCH) == 0:
            print("waiting reverse")
            sleep(1)
        max_position = stepper.get_current_position()
        print(f"Max reverse position: {max_position}")

        # Test setting angles
        angles = [-45, -90, -135, -180]
        for angle in angles:
            stepper.set_target_position(int(angle /
                                            (max_angle / abs(max_position))))
            sleep(5)
            print("Current position: ", stepper.get_current_position())

        # Shutdown stepper
        stepper.go_home_forward()
        while (stepper.get_variable(stepper.MISC_FLAGS, 1)[0] &
               stepper.HOMING_ACTIVE) != 0:
            sleep(1)
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.go_home_forward()
        while (stepper.get_variable(stepper.MISC_FLAGS, 1)[0] &
               stepper.HOMING_ACTIVE) != 0:
            sleep(1)
        stepper.de_energize()


if __name__ == "__main__":
    main()
