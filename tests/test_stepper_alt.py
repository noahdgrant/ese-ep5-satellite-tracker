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
        i2c_address = 0x0E

        stepper = Stepper(bus, i2c_address)
        stepper.init_limit_switch_forward()
        stepper.init_limit_switch_reverse()

#        while True:
#            switch = bus.read_byte_data(i2c_address, 0x01)
#            print(f"Limit switch: {switch}")
#            sleep(1)

        # Test limit switches
#        pos = stepper.get_current_position()
#        print(f"Pos: {pos}")
#        stepper.go_home_forward()
#        sleep(1)
#        while (stepper.get_variable(0x01, 1)[0] & 0x10) == 0:
#            print("wating forward")
#            sleep(1)
#        pos = stepper.get_current_position()
#        print(f"Pos: {pos}")
        stepper.go_home_forward()
        print("going forward")
        while (stepper.get_variable(0x01, 1)[0] & 0x10) != 0:
            print("wating forward")
            sleep(1)
        pos = stepper.get_current_position()
        print(f"Pos: {pos}")
        
        stepper.set_target_velocity(-3200000)
        print("going reverse")
        while (stepper.get_variable(0x01, 1)[0] & 0x8) == 0:
            print("wating reverse")
            sleep(1)
        pos = stepper.get_current_position()
        print(f"Pos: {pos}")
        
        stepper.set_target_position(int(pos/2))
        sleep(5)
#        stepper.go_home_reverse()
#        sleep(10)
#
        # Test setting angles
#        angles = [-45, -90, -135, -180]
#        for angle in angles:
#            stepper.set_target_position(int(angle / STEPPER_DEG_PER_32_STEP))
#            sleep(5)
#            pos = stepper.get_variable(0x02, 4)
#            print(f"Pos: {pos}")
#            pos = stepper.get_current_position()
#            print(f"Pos: {pos}")

        # Disable stepper
#        stepper.go_home_forward()
#        sleep(10)
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.go_home_forward()
        stepper.de_energize()


if __name__ == "__main__":
    main()