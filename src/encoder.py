# Tile: Encoder class for satellite tracker
# Author: Selman Bursal
# Date: November 23, 2023

import time


class Encoder:
    def __init__(self, bus, channel):
        self.AS5600_ADDRESS = 0x36
        self.MUX_ADDRESS = 0x70
        self.ANGLE_REGISTER_HIGH = 0x0E
        self.ANGLE_REGISTER_LOW = 0x0F
        self.bus = bus
        self.zero_deg_raw_value = None
        self.channel = channel
        self.position_north = 0

    def read_angle(self):
        self.enable_channel()
        high_byte = self.bus.read_byte_data(self.AS5600_ADDRESS,
                                            self.ANGLE_REGISTER_HIGH)
        low_byte = self.bus.read_byte_data(self.AS5600_ADDRESS,
                                           self.ANGLE_REGISTER_LOW)
        angle_raw = (high_byte << 8) | low_byte
        angle_deg = (angle_raw * 360) / 4096
        return angle_deg

    def calibrate_zero_degree(self):
        self.enable_channel()
        self.zero_deg_raw_value = (
                self.bus.read_byte_data(
                    self.AS5600_ADDRESS, self.ANGLE_REGISTER_HIGH << 8) |
                self.bus.read_byte_data(self.AS5600_ADDRESS,
                                        self.ANGLE_REGISTER_LOW))

    def get_adjusted_angle(self):
        if self.zero_deg_raw_value is None:
            print("Error: Calibration not performed." +
                  "Call calibrate_zero_degree() first.")
            return None

        angle = self.read_angle()
        adjusted_angle = angle - ((self.zero_deg_raw_value * 360)) / 4096
        adjusted_angle %= 360
        return adjusted_angle

    def enable_channel(self):
        self.bus.write_byte(self.MUX_ADDRESS, 1 << self.channel)
        time.sleep(0.1)
