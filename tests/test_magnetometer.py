#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from time import sleep
import board
from src.magnetometer import Magnetometer
from src.encoder import Encoder
from src.stepper import Stepper
from smbus2 import SMBus
import busio


def main():
    try:
        bus = board.I2C()
        i2c_address = 0x1E
        magnetometer = Magnetometer(bus, i2c_address)

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

        print("Displaying readings from magnetometer")

        # Test loop
        stepper.set_target_velocity(100000000)
        while True:
            angle = encoder.get_adjusted_angle()
            reading = magnetometer.get_heading()
            if 0 <= angle < 359.9:
                print("Encoder angle: ", angle)
                print("magnometer is reading: ", reading)
            else:
                break

        print("Loop finished...")
        stepper.de_energize()

    except KeyboardInterrupt:
        print("Quitting...")


if __name__ == "__main__":
    main()
