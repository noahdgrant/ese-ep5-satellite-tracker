#!/bin/python3

# Antenna class for satellite tracker

from stepper import Stepper
# from magnetometer import Magnetometer
from smbus2 import SMBus

I2C_ADDRESS_STEPPER_ALT = 14
I2C_ADDRESS_STEPPER_AZI = 15
I2C_ADDRESS_MAGNETOMETER = 30

STEPPER_DEG_PER_FULL_STEP = 1.8
STEPPER_DEG_PER_32_STEP = STEPPER_DEG_PER_FULL_STEP / 32
STEPPER_STEPS_PER_360_DEG = 360 / STEPPER_DEG_PER_32_STEP

STEPPER_ALT_MIDDLE_POS = 90 / STEPPER_DEG_PER_32_STEP
STEPPER_ALT_MAX_POS = 180 / STEPPER_DEG_PER_32_STEP
STEPPER_ALT_MIN_POS = 0


class Antenna():
    def __init__(self):
        self.stepper_azi_home_position = 0

        self.bus = SMBus(1)
        # self.magnetometer = Magnetometer(self.bus, I2C_ADDRESS_MAGNETOMETER)
        self.stepper_alt = Stepper(self.bus, I2C_ADDRESS_STEPPER_ALT)
        # self.stepper_azi = Stepper(self.bus, I2C_ADDRESS_STEPPER_AZI)

        self.stepper_alt.init_limit_switch_forward()
        self.stepper_alt.init_limit_switch_reverse()

    def alt_home(self):
        self.stepper_alt.go_home_forward()
        self.stepper_alt.set_target_position(STEPPER_ALT_MIDDLE_POS)

    def alt_set_angle(self, angle):
        position = STEPPER_ALT_MIDDLE_POS - (angle / STEPPER_DEG_PER_32_STEP)

        if position > STEPPER_ALT_MAX_POS:
            position = STEPPER_ALT_MAX_POS
        elif position < STEPPER_ALT_MIN_POS:
            position = STEPPER_ALT_MIN_POS

        self.stepper_alt.set_target_position(position)

    def azi_home(self):
        magnetometer_max = 0

        for step in range(STEPPER_STEPS_PER_360_DEG):
            self.stepper_azi.set_target_position(step)
            reading = self.magnetometer.get_value()
            if reading > magnetometer_max:
                magnetometer_max = reading
                self.stepper_azi_home_position = step

        self.stepper_azi.set_target_position(self.stepper_azi_home_position)

    def azi_set_angle(self, angle):
        position = (self.stepper_azi_home_position +
                    (angle / STEPPER_DEG_PER_32_STEP))
        self.stepper_azi.set_target_position(position)

    def home(self):
        # self.azi_home()
        self.alt_home()

    def shutdown(self):
        self.stepper_alt.go_home_forward()
        self.stepper_alt.de_energize()
        # self.stepper_azi.de_energize()
