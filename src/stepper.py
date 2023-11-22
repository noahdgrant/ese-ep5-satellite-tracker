#!/bin/python3

# Tile: Stepper motor control
# Author: Noah Grant
# Date: November 10, 2023

# This code is adapated from: https://www.pololu.com/docs/0J71/12.9

from smbus2 import i2c_msg


class Stepper:
    def __init__(self, bus, i2c_address):
        self.bus = bus
        self.i2c_address = i2c_address

        self.current_pos = 0

        self.exit_safe_start()
        self.energize()

    def energize(self):
        command = [0x85]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def exit_safe_start(self):
        command = [0x83]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def de_energize(self):
        command = [0x86]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def go_home_forward(self):
        command = [0x97, 0x01]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def go_home_reverse(self):
        command = [0x97, 0x00]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def get_variable(self, offset, length):
        write = i2c_msg.write(self.i2c_address, [0xA1, offset])
        read = i2c_msg.read(self.i2c_address, length)
        self.bus.i2c_rdwr(write, read)
        return list(read)

    def get_current_position(self):
        data = self.get_variable(0x22, 4)
        self.current_pos = (data[0] + (data[1] << 8) + (data[2] << 16) +
                            (data[3] << 24))
        if self.current_pos >= (1 << 31):
            self.current_pos -= (1 << 32)
        return self.current_pos

    def init_limit_switch_forward(self):
        # TX pin
        self.bus.write_byte_data(self.i2c_address, 0x3D, 0x08)        
#        command = [0x3D, 0x08]
#        write = i2c_msg.write(self.i2c_address, command)
#        self.bus.i2c_rdwr(write)

    def init_limit_switch_reverse(self):
        # RX pin
        command = [0x3E, 0x09]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

        command = [0x60, 0x06]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def set_target_position(self, target):
        command = [0xE0,
                   target >> 0 & 0xFF,
                   target >> 8 & 0xFF,
                   target >> 16 & 0xFF,
                   target >> 24 & 0xFF]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def set_target_velocity(self, target):
        command = [0xE3,
                   target >> 0 & 0xFF,
                   target >> 8 & 0xFF,
                   target >> 16 & 0xFF,
                   target >> 24 & 0xFF]
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)