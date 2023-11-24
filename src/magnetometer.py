# Tile: Magnetometer class for satellite tracker
# Author: Brendan
# Date: November 23, 2023

from math import atan2, degrees


class Magnetometer():
    def __init__(self, bus, i2c_address):
        set_ccm = 0x22
        self.x_msb = 0x29
        self.x_lsb = 0x28
        self.y_msb = 0x2B
        self.y_lsb = 0x2A

        self.bus = bus
        self.i2c_address = i2c_address

        self.bus.write_byte_data(self.i2c_address, set_ccm, 0)

    # call repeatedly
    def read_mag(self, mag_addr):
        x_raw = self.bus.read_i2c_block_data(mag_addr, self.x_lsb, 2)
        y_raw = self.bus.read_i2c_block_data(mag_addr, self.y_lsb, 2)

        x_l = x_raw >> 8
        x_h = x_raw & 0xFF00
        x = x_l % x_h

        y_l = y_raw >> 8
        y_h = y_raw & 0xFF00
        y = y_l % y_h

        return (x, y)
