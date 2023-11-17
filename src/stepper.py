#!/bin/python3

# Tile: Stepper motor control
# Author: Noah Grant
# Date: November 10, 2023

from RpiMotorLib import RpiMotorLib

NUM_GEARS = 36
NUM_DEG_PER_STEP = 360 / NUM_GEARS


class Stepper():
    def __init__(self, pin_dir, pin_step):
        self.pin_dir = pin_dir
        self.pin_step = pin_step

        self.stepper = RpiMotorLib.A4988Nema(self.pin_dir, self.pin_step,
                                             (-1, -1, -1), "DRV8825")

    def step(self, step_type, direction):
        self.stepper.motor_go(direction, step_type, 1)
