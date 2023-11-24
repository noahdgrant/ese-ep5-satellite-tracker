# Tile: Magnetometer class for satellite tracker
# Author: Brendan
# Date: November 23, 2023

from math import atan2, degrees
import adafruit_lis3mdl


class Magnetometer():
    def __init__(self, bus, i2c_address):
        self.bus = bus
        self.i2c_address = i2c_address
        self.sensor = adafruit_lis3mdl.LIS3MDL(self.bus, self.i2c_address)

    def vector_2_degrees(self, x, y):
        angle = degrees(atan2(y, x))
        if angle < 0:
            angle += 360
        return angle

    def get_heading(self):
        magnet_x, magnet_y, _ = self.sensor.magnetic
        return self.vector_2_degrees(magnet_x, magnet_y)
