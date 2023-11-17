#!/bin/python3

# Antenna class for satellite tracker

from stepper import Stepper
from magnetometer import Magnetometer
from limit_switch import Limit_Switch

STEPPER_DEG_PER_FULL_STEP = 1.8


class Antenna():
    def __init__(self):
        self.stepper_alt = Stepper()
        self.stepper_azi = Stepper()
        self.magnetometer = Magnetometer()
        self.limit_switch_noth = Limit_Switch()
        self.limit_switch_south = Limit_Switch()

        self.magnetometer_max = 0
        self.stepper_alt_count = 0

    def alt_home(self):
        # Tilt to North face
        while self.limit_switch_north.limit is False:
            self.stepper_alt.step("Full", False)

        self.stepper_alt_count = 0

        # Tilt to South Face
        while self.limit_switch_south.limit is False:
            self.stepper_alt.step("Full", True)
            self.stepper_alt_count += 1

        # Point straight up
        for _ in range(self.stepper_alt_count / 2):
            self.stepper_alt.step("Full", False)

        self.stepper_alt_count /= 2

    def alt_set_angle(self, angle):
        ...

    def azi_home(self):
        self.magnetometer_max = 0

        # Find North
        for _ in range(360/STEPPER_DEG_PER_FULL_STEP):
            self.stepper_azi.step("Full", False)
            magnetometer_reading = self.magnetometer.read()

            if magnetometer_reading > self.magnetometer_max:
                self.magnetometer_max = magnetometer_reading

        # Point North
        while self.magnetometer.read() < (self.magnetometer_max - 5):
            self.stepper_azi.step("Full", False)

    def azi_set_angle(self, angle):
        ...

    def home(self):
        self.azi_home()
        self.alt_home()
