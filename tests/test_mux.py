import sys
sys.path.append("..")

from src.encoder import Encoder
from time import sleep
from smbus2 import SMBus

ALT_CHANNEL = 0
AZ_CHANNEL = 1


def main():
    # Initialize encoder
    bus = SMBus(11)

    encoder_az = Encoder(bus, AZ_CHANNEL)
    encoder_alt = Encoder(bus, ALT_CHANNEL)
    # Calibration
    # input("Place the sensor in a known orientation (e.g., zero degree position) and press Enter to calibrate.")
    encoder_az.calibrate_zero_degree()
    encoder_alt.calibrate_zero_degree()

    print("Calibration completed. Script will now run.")

    try:
        while True:
            angle_az = encoder_az.get_adjusted_angle()
            angle1_az = encoder_az.read_angle()

            angle_alt = encoder_alt.get_adjusted_angle()
            angle1_alt = encoder_alt.read_angle()

            print("Alt:")
            print(f"Adjusted Angle: {angle_alt:.2f} degrees")
            print(f"Real Angle: {angle1_alt:.2f} degrees")

            print("Az:")
            print(f"Adjusted Angle: {angle_az:.2f} degrees")
            print(f"Real Angle: {angle1_az:.2f} degrees")

            sleep(1)

    except KeyboardInterrupt:
        print("Script terminated by the user.")


if __name__ == "__main__":
    main()
