#!/bin/python3

# Tile: Stepper motor control
# Author: Noah Grant
# Date: November 10, 2023

import RPi.GPIO as GPIO
from RpiMotorLib import RpiMotorLib

NUM_GEARS = 36
NUM_DEG_PER_STEP = 360 / NUM_GEARS


class Stepper():
    def __init__(self, pin_dir, pin_step, pin_en):
        self.motor = RpiMotorLib.A4988Nema(pin_dir, pin_step, (-1, -1, -1),
                                           "DRV8825")

        self.step_count = 0
        self.angle_old = 0
        self.angle_cur = 0

    def home_alt(self):
        self.angle_old = 0
        self.angle_cur = 0

    def home_azi(self):
        ...

    def set_angle(self, angle):
        # Calculate steps for new angle
        self.angle_old = self.angle_cur
        self.angle_cur = angle

        num_steps = int((self.angle_cur - self.angle_old) / NUM_DEG_PER_STEP)
        self.step_count += num_steps

        # Output new angle
        ...
