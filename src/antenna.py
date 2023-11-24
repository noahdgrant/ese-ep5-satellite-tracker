# Tile: Antenna class for satellite tracker
# Author: Noah Grant
# Date: November 22, 2023

from .stepper import Stepper
from .magnetometer import Magnetometer
from .encoder import Encoder
from smbus2 import SMBus
from time import sleep
import board

# I2C addresses
I2C_ADDRESS_STEPPER_ALT = 0x0E
I2C_ADDRESS_STEPPER_AZI = 0x0F
I2C_ADDRESS_MAGNETOMETER = 0x1E
I2C_ADDRESS_ENCODER_ALT = ...
I2C_ADDRESS_ENCODER_AZI = 0x36


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
        self.azi_total_steps = 0

        # I2C setup
        self.bus = SMBus(11)
        self.bus2 = board.I2C()
        self.magnetometer = Magnetometer(self.bus2, I2C_ADDRESS_MAGNETOMETER)
        self.stepper_alt = Stepper(self.bus, I2C_ADDRESS_STEPPER_ALT)
        self.stepper_azi = Stepper(self.bus, I2C_ADDRESS_STEPPER_AZI)
        self.encoder_azi = Encoder(self.bus, I2C_ADDRESS_STEPPER_AZI)

        # Altitude stepper setup
        self.stepper_alt.max_degree = 180
        self.stepper_alt.init_limit_switch_forward()
        self.stepper_alt.init_limit_switch_reverse()

        # Azimuth stepper setup
        self.stepper_azi_home_position = 0

    def go_alt_home(self):
        # Go to forward home position
        self.stepper_alt.go_home_forward()
        while (self.stepper_alt.get_variable(
            self.stepper_alt.MISC_FLAGS, 1)[0] &
               self.stepper_alt.HOMING_ACTIVE) != 0:
            sleep(1)
        self.alt_position_min = self.stepper_alt.get_current_position()

        # Go to reverse max position
        self.stepper_alt.set_target_velocity(-3200000)
        while (self.stepper_alt.get_variable(
            self.stepper_alt.MISC_FLAGS, 1)[0] &
               self.stepper_alt.REVERSE_LIMIT_SWITCH) == 0:
            sleep(1)
        self.alt_position_max = self.stepper_alt.get_current_position()
        self.alt_position_home = self.alt_position_max / 2

        # Go to midway point
        self.stepper_alt.set_target_position(self.alt_position_home)

    def go_azi_home(self):
        # Go to North
        self.stepper_azi.set_target_velocity(100000000)
        while self.magnetometer.get_heading() > 1:
            pass
        self.stepper_azi.set_target_velocity(0)

        # Count number of steps in a full rotation
        self.azi_position_min = self.stepper_azi.get_current_position()
        self.encoder_azi.calibrate_zero_degree()
        self.stepper_azi.set_target_velocity(100000000)
        while 0 < self.encoder_azi.get_adjusted_angle() < 359.9:
            pass
        self.stepper_azi.set_target_velocity(0)
        self.azi_position_max = self.stepper_azi.get_current_position()
        self.azi_total_steps = abs(
                self.azi_position_max - self.azi_position_min)

        # Calibrate azimuth encoder
        self.encoder_azi.calibrate_zero_degree()

    def go_home(self):
        self.azi_home()
        self.alt_home()

    def set_alt_angle(self, angle):
        if angle > self.alt_angle_max:
            angle = self.alt_angle_max
        elif angle < self.alt_angle_min:
            angle = self.alt_angle_min
        self.stepper_alt.set_target_position(
                int(angle / (self.alt_angle_max / abs(self.alt_position_max))))

    def set_azi_angle(self, angle):
        if angle > self.azi_angle_max:
            angle = self.azi_angle_max
        elif angle < self.azi_angle_min:
            angle = self.azi_angle_min
        self.stepper_azi.set_target_position(
                int(angle / (self.azi_angle_max / self.azi_total_steps)))

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
