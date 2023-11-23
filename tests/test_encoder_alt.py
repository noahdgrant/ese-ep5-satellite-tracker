import sys
sys.path.append("..")

from src.encoder import Encoder
from time import sleep
from smbus2 import SMBus

def main():
    # Initialize encoder
    bus = SMBus(11)
    i2c_address = 0x36

    encoder = Encoder(bus, i2c_address)

    # Calibration
    input("Place the sensor in a known orientation (e.g., zero degree position) and press Enter to calibrate.")
    encoder.calibrate_zero_degree()
    print("Calibration completed. Script will now run.")

    try:
        while True:
            angle = encoder.get_adjusted_angle()

            if angle is not None:
                print(f"Adjusted Angle: {angle:.2f} degrees")

            sleep(1)

    except KeyboardInterrupt:
        print("Script terminated by the user.")

if __name__ == "__main__":
    main()
