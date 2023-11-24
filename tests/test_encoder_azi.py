#!/bin/python3

# AS5600 magnetic position encoder testing mainline (azimuth)


import sys
sys.path.append("..")

from src.encoder import Encoder
from src.stepper import Stepper
from time import sleep
from smbus2 import SMBus


def main():
    try:
        # Initialize encoder
        bus = SMBus(11)
        i2c_address_encoder = 0x36
        encoder = Encoder(bus, i2c_address_encoder)

        i2c_address_stepper = 0x0F
        stepper = Stepper(bus, i2c_address_stepper)

        # Calibration
        encoder.calibrate_zero_degree()
        angle = encoder.get_adjusted_angle()
        print("Encoder angle: %d", angle)

        # Test loop
        stepper.set_target_velocity(100000000)
        while True:
            angle = encoder.get_adjusted_angle()
            if 0 <= angle < 359.9:
                print("Encoder angle: ", angle)
            else:
                break

        print("Loop finished...")
        stepper.de_energize()

    except KeyboardInterrupt:
        stepper.de_energize()
        print("Script terminated by the user.")


if __name__ == "__main__":
    main()
