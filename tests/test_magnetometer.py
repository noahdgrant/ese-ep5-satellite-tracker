#!/bin/python3

# Adafruit MMC5603 magnetometer testing mainline

import sys
sys.path.append("..")

from smbus2 import SMBus
from src.magnetometer import Magnetometer
from time import sleep
import math

REG_WHO_AM_I = 0x0F
REG_CTRL_REG1 = 0x20
REG_CTRL_REG2 = 0x21
REG_CTRL_REG3 = 0x22
REG_CTRL_REG4 = 0x23
REG_CTRL_REG5 = 0x24
REG_STATUS_REG = 0x27
REG_OUT_X_L = 0x28
REG_OUT_X_H = 0x29
REG_OUT_Y_L = 0x2A
REG_OUT_Y_H = 0x2B
REG_OUT_Z_L = 0x2C
REG_OUT_Z_H = 0x2D
REG_TEMP_OUT_L = 0x2E
REG_TEMP_OUT_H = 0x2F
REG_INT_CFG = 0x30
REG_INT_SRC = 0x31
REG_INT_THS_L = 0x32
REG_INT_THS_H = 0x33

offset_x = 0
offset_y = 0
offset_z = 0


def main():
    # LIS3MDL Registers
    # Initialize I2C bus
    bus = SMBus(1)
    address = 0x1E

    # Initialize LIS3MDL
    bus.write_byte_data(address, REG_CTRL_REG1, 0x70)  # Set sample rate to 80Hz
    bus.write_byte_data(address, REG_CTRL_REG2, 0x00)  # Set scale to 4 gauss
    bus.write_byte_data(address, REG_CTRL_REG3, 0x00)  # Set continuous conversion mode
    bus.write_byte_data(address, REG_CTRL_REG1, 0x60)  # Set X and Y to ultra high performance mode
    bus.write_byte_data(address, REG_CTRL_REG4, 0x0C)  # Set Z operative mode to high-performance mode

    def calibrate():
        print("Calibrating magnetometer. Please rotate the sensor around all axes...")
        x, y, z = get_reading()
        min_x = max_x = x
        min_y = max_y = y
        min_z = max_z = z

        for i in range(2000):
            x, y, z = get_reading()

            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)

            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)

            sleep(0.01)

        # Calculate the middle of the min/max range
        offset_x = (max_x + min_x) / 2
        offset_y = (max_y + min_y) / 2
        offset_z = (max_z + min_z) / 2

        print("Calibration done")
        print(f"x offset = {offset_x}, y offset = {offset_y}, z offset = {offset_z}")

    # Function to read sensor data
    def get_reading():
        data = bus.read_i2c_block_data(address, REG_OUT_X_L, 6)
        x = data[0] | (data[1] << 8)
        y = data[2] | (data[3] << 8)
        z = data[4] | (data[5] << 8)

        if x > 32767:
            x -= 65536
        if y > 32767:
            y -= 65536
        if z > 32767:
            z -= 65536

        return (x, y, z)

    def get_heading():
        x, y, _ = get_reading()
        x -= offset_x
        y -= offset_y
        return vector_to_degrees(x, y)

    def vector_to_degrees(x, y):
        # Calculate heading
        angle = math.degrees(math.atan2(y, x))
        if angle < 360:
            angle += 360
        return angle

    calibrate()

    while True:
        print("Heading: {:.2f} degrees".format(get_heading()))


if __name__ == "__main__":
    main()
