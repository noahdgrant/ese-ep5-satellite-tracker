# Tile: Magnetometer class for satellite tracker
# Author: Noah Grant
# Date: November 23, 2023


class Magnetometer():
    def __init__(self, bus, i2c_address):
        self.ADDRESS_X_AXIS = 0x28
        self.ADDRESS_Y_AXIS = 0x2A

        self.bus = bus
        self.i2c_address = i2c_address

    def get_reading(self):
        x_data = self.bus.read_i2c_block_data(self.i2c_address,
                                              self.ADDRESS_X_AXIS, 2)
        y_data = self.bus.read_i2c_block_data(self.i2c_address,
                                              self.ADDRESS_Y_AXIS, 2)
        return x_data, y_data
