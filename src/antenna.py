# Tile: Antenna class for satellite tracker
# Author: Noah Grant
# Date: November 22, 2023

from .stepper import Stepper
from .magnetometer import Magnetometer
from smbus2 import SMBus
from time import sleep

# I2C addresses
I2C_ADDRESS_STEPPER_ALT = 0x0E
I2C_ADDRESS_STEPPER_AZI = 0x0F
I2C_ADDRESS_MAGNETOMETER = 0x1E
I2C_ADDRESS_ENCODER_ALT = 0x36
I2C_ADDRESS_ENCODER_AZI = ...


class Antenna():
    def __init__(self):
        # Antenna characteristics
        self.alt_angle_min = 0
        self.alt_angle_max = 180
        self.alt_position_home = 0
        self.alt_position_min = 0
        self.alt_position_max = 0

        self.azi_angle_min = 0
        self.azi_angle_max = 360
        self.azi_position_min = 0
        self.azi_position_max = 0

        # I2C setup
        self.bus = SMBus(1)
        self.magnetometer = Magnetometer(self.bus, I2C_ADDRESS_MAGNETOMETER)
        self.stepper_alt = Stepper(self.bus, I2C_ADDRESS_STEPPER_ALT)
        self.stepper_azi = Stepper(self.bus, I2C_ADDRESS_STEPPER_AZI)

        # Altitude stepper setup
        self.stepper_alt.max_degree = 180
        self.stepper_alt.init_limit_switch_forward()
        self.stepper_alt.init_limit_switch_reverse()

        # Azimuth stepper setup
        self.stepper_azi_home_position = 0

    def go_alt_home(self):
        self.stepper_alt.go_home_forward()
        while (self.stepper_alt.get_variable(
            self.stepper_alt.MISC_FLAGS, 1)[0] &
               self.stepper_alt.HOMING_ACTIVE) != 0:
            sleep(1)
        self.alt_position_min = self.stepper_alt.get_current_position()

        self.stepper_alt.set_target_velocity(-3200000)
        while (self.stepper_alt.get_variable(
            self.stepper_alt.MISC_FLAGS, 1)[0] &
               self.stepper_alt.REVERSE_LIMIT_SWITCH) == 0:
            sleep(1)
        self.alt_position_max = self.stepper_alt.get_current_position()
        self.alt_position_home = self.alt_position_max / 2
        self.stepper_alt.set_target_position(self.alt_position_home)

    def go_azi_home(self):
        # save current stepper position to azi_position_min
        # set encoder angle to 0
        # set stepper velocity to a medium speed
        # while encoder angle < 360:
        #   read magnetometer value
        #   if magnetometer value > max magnetometer value that has been read
        #       update max magnetometer value
        #       save current stepper position to azi_position_max
        # go to stepper position where max magentometer value was read
        # set encoder angle to 0

        # ?? do we maybe change to values of azi_position_min and
        # azi_position_max once this is done to make them line up with North?
        ...

    def go_home(self):
        self.azi_home()
        self.alt_home()

    def set_alt_angle(self, angle):
        if angle > self.alt_angle_max:
            angle = self.alt_angle_max
        elif angle < self.alt_angle_min:
            angle = self.alt_angle_min
        self.stepper_alt.set_target_position(
                int(angle / (self.alt_angle_max / self.alt_position_max)))

    def set_azi_angle(self, angle):
        if angle > self.azi_angle_max:
            angle = self.azi_angle_max
        elif angle < self.azi_angle_min:
            angle = self.azi_angle_min
        self.stepper_azi.set_target_position(
                int(angle / (self.azi_angle_max / self.azi_position_max)))

    def shutdown(self):
        # Shutdown altitude stepper
        self.stepper_alt.go_home_forward()
        while (self.stepper_alt.get_variable(
            self.stepper_alt.MISC_FLAGS, 1)[0] &
               self.stepper_alt.HOMING_ACTIVE) != 0:
            sleep(1)
        self.stepper_alt.de_energize()

        # Shutdown azimuth stepper
        self.stepper_azi.de_energize()
