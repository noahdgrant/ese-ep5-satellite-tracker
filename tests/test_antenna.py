#!/bin/python3

# Testing mainline for Antenna class

from src.antenna import Antenna


def main():
    antenna = Antenna()

    # Test homing altitude
    # Expected result: antenna points straight up
    antenna.home()

    # Test setting angles
    # Expected result: antenna points 45 deg towards North
    antenna.alt_set_angle(45)

    # Expected result: antenna points 180 deg towards North
    antenna.alt_set_angle(180)

    # Expected result: antenna points straight up
    antenna.alt_set_angle(0)

    # Expected result: antenna points 45 deg towards South
    antenna.alt_set_angle(-45)

    # Expected result: antenna points 180 deg towards South
    antenna.alt_set_angle(-180)

    # Test shutdown sequence
    # Expected result: antenna altitude stepper returns to home position
    # (180 deg) and de-energizes
    antenna.shutdown()


if __name__ == "__main__":
    main()
