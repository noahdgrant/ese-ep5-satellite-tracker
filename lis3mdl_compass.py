# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display compass heading data five times per second """
import time
from math import atan2, degrees
import board
import adafruit_lis3mdl

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_lis3mdl.LIS3MDL(i2c, 0x1e)

offset_x = -91.92
offset_y = -27.81
offset_z = 29.44


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


def get_heading(_sensor):
    magnet_x, magnet_y, _ = _sensor.magnetic
    magnet_x -= offset_x
    magnet_y -= offset_y
    return vector_2_degrees(magnet_x, magnet_y)


while True:
    print("heading: {:.2f} degrees".format(get_heading(sensor)))
    time.sleep(0.2)
