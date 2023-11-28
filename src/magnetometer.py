# Tile: Magnetometer class for satellite tracker
# Author: Noah Grant
# Date: November 28, 2023

from math import atan2, degrees
from time import sleep

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


class Magnetometer():
    def __init__(self, bus, i2c_address):
        self.bus = bus
        self.i2c_address = i2c_address

        # Set X and Y to ultra high-performance mode
        self.bus.write_byte_data(self.i2c_address, REG_CTRL_REG1, 0x60)
        # Set Z to ultra high-performance mode
        self.bus.write_byte_data(self.i2c_address, REG_CTRL_REG4, 0x0C)
        # Set sample rate to 155Hz
        self.bus.write_byte_data(self.i2c_address, REG_CTRL_REG1, 0x02)
        # Set scale to 4 gauss
        self.bus.write_byte_data(self.i2c_address, REG_CTRL_REG2, 0x00)
        # Set continuous conversion mode
        self.bus.write_byte_data(self.i2c_address, REG_CTRL_REG3, 0x00)

        self.offset_x = -91.92
        self.offset_y = -27.81
        self.offset_z = 29.44

        sleep(0.010)

    def calibrate(self):
        print("Calibrating magnetometer.")
        print("Please rotate the sensor around all axes...")
        x, y, z = self.get_reading()
        min_x = max_x = x
        min_y = max_y = y
        min_z = max_z = z

        for i in range(2000):
            x, y, z = self.get_reading()

            min_x = min(min_x, x)
            min_y = min(min_y, y)
            min_z = min(min_z, z)

            max_x = max(max_x, x)
            max_y = max(max_y, y)
            max_z = max(max_z, z)

            sleep(0.01)

        # Calculate the middle of the min/max range
        self.offset_x = (max_x + min_x) / 2
        self.offset_y = (max_y + min_y) / 2
        self.offset_z = (max_z + min_z) / 2

        print("Calibration done")
        print(f"x offset = {self.offset_x:6.2f}, " +
              f"y offset = {self.offset_y:6.2f}, " +
              f"z offset = {self.offset_z:6.2f}")

    def get_heading(self):
        x, y, _ = self.get_reading()
        x -= self.offset_x
        y -= self.offset_y
        return self.vector_to_degrees(x, y)

    def get_reading(self):
        data = self.bus.read_i2c_block_data(self.i2c_address, REG_OUT_X_L, 6)
        x = data[0] | (data[1] << 8)
        y = data[2] | (data[3] << 8)
        z = data[4] | (data[5] << 8)

        x = (x / 6842) * 100
        y = (y / 6842) * 100
        z = (z / 6842) * 100

        return (x, y, z)

    def vector_to_degrees(self, x, y):
        angle = degrees(atan2(y, x))
        if angle < 0:
            angle += 360
        return angle
