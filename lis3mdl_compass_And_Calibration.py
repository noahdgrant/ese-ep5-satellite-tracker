# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

""" Display compass heading data five times per second """
import time
from math import atan2, degrees
import board
import adafruit_lis3mdl
#========================================Calbration============================================#
import busio
from adafruit_lis3mdl import LIS3MDL
SAMPLE_SIZE = 2000

i2c = busio.I2C(board.SCL, board.SDA)
magnetometer = LIS3MDL(i2c)

while True:
    print("=" * 40)
    print("LIS3MDL MAGNETOMETER CALIBRATION")
    print("  Tumble the sensor through a series of")
    print("  overlapping figure-eight patterns")
    print(f"  for approximately {SAMPLE_SIZE/100:.0f} seconds \n")

    print("  countdown to start:", end=" ")
    for i in range(5, -1, -1):
        print(i, end=" ")
        time.sleep(1)
    print("\n  MOVE the sensor...")
    print("  >     progress     <")
    print("  ", end="")

    # Initialize the min/max values
    mag_x, mag_y, mag_z = magnetometer.magnetic
    min_x = max_x = mag_x
    min_y = max_y = mag_y
    min_z = max_z = mag_z

    for i in range(SAMPLE_SIZE):
        # Capture the samples and show the progress
        if not i % (SAMPLE_SIZE / 20):
            print("*", end="")

        mag_x, mag_y, mag_z = magnetometer.magnetic

        min_x = min(min_x, mag_x)
        min_y = min(min_y, mag_y)
        min_z = min(min_z, mag_z)

        max_x = max(max_x, mag_x)
        max_y = max(max_y, mag_y)
        max_z = max(max_z, mag_z)

        time.sleep(0.01)

    # Calculate the middle of the min/max range
    offset_x = (max_x + min_x) / 2
    offset_y = (max_y + min_y) / 2
    offset_z = (max_z + min_z) / 2

    print(
        f"\n\n  Final Calibration: X:{offset_x:6.2f} Y:{offset_y:6.2f} Z:{offset_z:6.2f} uT\n"
    )

    CMD = input("\nAre you satisfied with your calibration? [Y/N]: ")
    if CMD == "y":
        break
    print("Restarting calibration......")
    time.sleep(5)

#==================================CALIBRATION END================================#

i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor = adafruit_lis3mdl.LIS3MDL(i2c)


def vector_2_degrees(x, y):
    angle = degrees(atan2(y, x))
    if angle < 0:
        angle += 360
    return angle


def get_heading(_sensor):
    magnet_x, magnet_y, _ = _sensor.magnetic
    return vector_2_degrees(magnet_x, magnet_y)


while True:
    print("heading: {:.2f} degrees".format(get_heading(sensor)))
    time.sleep(0.2)
