# Tile: Antenna class for satellite tracker
# Author: Noah Grant
# Date: November 22, 2023

from .stepper import Stepper
# from .magnetometer import Magnetometer
from smbus2 import SMBus
from time import sleep

# I2C addresses
I2C_ADDRESS_STEPPER_ALT = 14
I2C_ADDRESS_STEPPER_AZI = 15
I2C_ADDRESS_MAGNETOMETER = 30

# TIC T834 stepper driver I2C addresses
MISC_FLAGS = 0x01
HOMING_ACTIVE = 0x10
REVERSE_LIMIT_SWITCH = 0x08


class Antenna():
    def __init__(self):
        self.stepper_azi_home_position = 0

        self.bus = SMBus(1)
        # self.magnetometer = Magnetometer(self.bus, I2C_ADDRESS_MAGNETOMETER)
        self.stepper_alt = Stepper(self.bus, I2C_ADDRESS_STEPPER_ALT)
        # self.stepper_azi = Stepper(self.bus, I2C_ADDRESS_STEPPER_AZI)

        # Altitude stepper setup
        self.stepper_alt.max_degree = 180
        self.stepper_alt.init_limit_switch_forward()
        self.stepper_alt.init_limit_switch_reverse()

    def go_alt_home(self):
        self.stepper_alt.go_home_forward()
        while (self.stepper_alt.get_variable(MISC_FLAGS, 1)[0] &
               HOMING_ACTIVE) != 0:
            sleep(1)

        self.stepper_alt.set_target_velocity(-3200000)
        while (self.stepper_alt.get_variable(MISC_FLAGS, 1)[0] &
               REVERSE_LIMIT_SWITCH) == 0:
            sleep(1)
        self.stepper_alt.max_position = self.stepper_alt.get_current_position()
        self.stepper_alt.home_position = self.stepper_alt.max_position / 2
        self.stepper_alt.set_target_position(self.stepper_alt.home_position)

    def go_azi_home(self):
        ...

    def go_home(self):
        # self.azi_home()
        self.alt_home()

    def set_alt_angle(self, angle):
        if angle > self.stepper_alt.max_angle:
            angle = self.stepper_alt.max_angle
        elif angle < self.stepper_alt.min_angle:
            angle = self.stepper_alt.min_angle
        self.stepper_alt.set_target_angle(angle)

    def set_azi_angle(self, angle):
        ...

    def shutdown(self):
        # Shutdown altitude stepper
        self.stepper_alt.go_home_forward()
        while (self.stepper_alt.get_variable(MISC_FLAGS, 1)[0] &
               HOMING_ACTIVE) != 0:
            sleep(1)
        self.stepper_alt.de_energize()

        # Shutdown azimuth stepper
        # self.stepper_azi.de_energize()
