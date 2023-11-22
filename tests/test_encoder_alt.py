import sys
sys.path.append("..")

from encoder import Encoder
import time

def main():
    encoder = Encoder()

    # Calibration
    input("Place the sensor in a known orientation (e.g., zero degree position) and press Enter to calibrate.")
    encoder.calibrate_zero_degree()
    print("Calibration completed. Script will now run.")

    try:
        while True:
            angle = encoder.get_adjusted_angle()

            if angle is not None:
                print(f"Adjusted Angle: {angle:.2f} degrees")

            time.sleep(1)

    except KeyboardInterrupt:
        print("Script terminated by user.")

if __name__ == "__main__":
    main()
