# Tile: encoder class for satellite tracker
# Author: Selman Bursal
# Date: November 23, 2023
# Version: 1.0

from smbus2 import SMBus
import time

class Encoder:
    def __init__(self, bus, i2c_address):
        self.AS5600_ADDRESS = i2c_address
        self.ANGLE_REGISTER_HIGH = 0x0E
        self.ANGLE_REGISTER_LOW = 0x0F
        self.bus = bus
        self.zero_deg_raw_value = None

    def read_angle(self):
        high_byte = self.bus.read_byte_data(self.AS5600_ADDRESS, self.ANGLE_REGISTER_HIGH)
        low_byte = self.bus.read_byte_data(self.AS5600_ADDRESS, self.ANGLE_REGISTER_LOW)
        angle_raw = (high_byte << 8) | low_byte
        angle_deg = (angle_raw * 360) / 4096 #2^12 = 4096 this is a 12 bit res 
        return angle_deg

    def calibrate_zero_degree(self):
        input("Rotate the sensor to the zero degree position and press Enter.")
        self.zero_deg_raw_value = (self.bus.read_byte_data(self.AS5600_ADDRESS, self.ANGLE_REGISTER_HIGH) << 8) | self.bus.read_byte_data(self.AS5600_ADDRESS, self.ANGLE_REGISTER_LOW)

    def get_adjusted_angle(self):
        if self.zero_deg_raw_value is None:
            print("Error: Calibration not performed. Call calibrate_zero_degree() first.")
            return None

        angle = self.read_angle()
        adjusted_angle = angle - ((self.zero_deg_raw_value * 360) + 90) / 4096 #this line need to be changed to fit our purpose 
        adjusted_angle %= 360
        return adjusted_angle
