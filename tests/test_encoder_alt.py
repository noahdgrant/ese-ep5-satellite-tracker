import sys
sys.path.append("..")

from src.encoder import Encoder
from time import sleep
from smbus2 import SMBus

ALT_CHANNEL = 0


def main():
    # Initialize encoder
    bus = SMBus(11)

    encoder = Encoder(bus, ALT_CHANNEL)

    # Calibration
    # input("Place the sensor in a known orientation (e.g., zero degree position) and press Enter to calibrate.")
    encoder.calibrate_zero_degree()
    print("Calibration completed. Script will now run.")

    try:
        while True:
            angle = encoder.get_adjusted_angle()
            angle1 = encoder.read_angle()

            if angle is not None:
                print(f"Adjusted Angle: {angle:.2f} degrees")
                print(f"Real Angle: {angle1:.2f} degrees")

            sleep(1)

    except KeyboardInterrupt:
        print("Script terminated by the user.")


if __name__ == "__main__":
    main()
