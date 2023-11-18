#!/bin/python3

# Antenna class for satellite tracker

from stepper import Stepper
from magnetometer import Magnetometer
from smbus2 import SMBus

I2C_ADDRESS_STEPPER_ALT = 14

STEPPER_DEG_PER_FULL_STEP = 1.8
STEPPER_DEG_PER_32_STEP = STEPPER_DEG_PER_FULL_STEP / 32


class Antenna():
    def __init__(self):
        self.bus = SMBus(1)

        self.stepper_alt = Stepper(self.bus, I2C_ADDRESS_STEPPER_ALT)
        self.stepper_azi = Stepper()
        self.magnetometer = Magnetometer()

        self.magnetometer_max = 0
        self.stepper_alt_count = 0

        self.stepper_alt.init_limit_switch_forward()
        self.stepper_alt.init_limit_switch_reverse()

    def alt_home(self):
        self.stepper_alt.go_home_forward()

    def alt_set_angle(self, angle):
        self.stepper_alt.set_target_position(-angle / STEPPER_DEG_PER_32_STEP)

    def azi_home(self):
        ...

    def azi_set_angle(self, angle):
        ...

    def home(self):
        self.azi_home()
        self.alt_home()

    def shutdown(self):
        self.stepper_alt.go_home_forward()
        self.stepper_alt.de_energize()
        self.stepper_azi.de_energize()
