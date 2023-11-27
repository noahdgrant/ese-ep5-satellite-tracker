# Tile: Stepper motor class for satellite tracker
# Author: Noah Grant
# Date: November 10, 2023

# This code is adapated from: https://www.pololu.com/docs/0J71/12.9

from smbus2 import i2c_msg


class Stepper:
    def __init__(self, bus, i2c_address):
        self.current_position = 0

        # I2C initialization
        self.bus = bus
        self.i2c_address = i2c_address

        # TIC T834 memory offsets and bit numbers
        self.MISC_FLAGS = 0x01
        self.HOMING_ACTIVE = 0x10
        self.REVERSE_LIMIT_SWITCH = 0x08

        # Start stepper
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
        self.current_position = (data[0] + (data[1] << 8) + (data[2] << 16) +
                                 (data[3] << 24))
        if self.current_position >= (1 << 31):
            self.current_position -= (1 << 32)
        return self.current_position

    def stop(self):
        # Get current position
        position = self.get_current_position()

        # Stop motor
        command = [0xEC, position] #was position[0] need to test
        write = i2c_msg.write(self.i2c_address, command)
        self.bus.i2c_rdwr(write)

    def init_limit_switch_forward(self):
        # TX pin
        self.bus.write_byte_data(self.i2c_address, 0x3D, 0x08)

    def init_limit_switch_reverse(self):
        # RX pin
        self.bus.write_byte_data(self.i2c_address, 0x3E, 0x09)

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
