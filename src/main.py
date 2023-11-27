#!/usr/bin/python3

# Title: ESE EP5 Satellite Tracker
# Author: Noah Grant
# Date: November 8, 2023

from datetime import datetime
import ephem
import geocoder
import requests
from time import sleep

from antenna import Antenna

# API links
TLE_URL = "http://tle.ivanstanojevic.me/api/tle/"
ELEVATION_URL = "https://api.open-elevation.com/api/v1/lookup?locations="

# Satellite information
SATELLITE_NUMBER = 25544  # ISS


def main():
    print("ESE EP5 Satellite Tracker\n")

    # Current latitude, longitude, and altitude
    location = geocoder.ip("me")
    elevation = requests.get(
            f"{ELEVATION_URL}{location.latlng[0]},{location.latlng[1]}"
            ).json()
    meters = elevation["results"][0]["elevation"]

    print("OBSERVER INFORMATION:")
    print(f"Latitude: {location.latlng[0]}")
    print(f"Longitude: {location.latlng[1]}")
    print(f"Elevation: {meters}m")

    # Setup observer
    observer = ephem.Observer()
    observer.lat, observer.lon = location.latlng

    # TLE info for satellite
    tle = requests.get(f"{TLE_URL}{SATELLITE_NUMBER}").json()
    satellite_name = tle["name"]
    satellite_line1 = tle["line1"]
    satellite_line2 = tle["line2"]
    satellite = ephem.readtle(satellite_name, satellite_line1,
                              satellite_line2)

    print("\nSATELLITE INFORMATION:")
    print(f"Name: {satellite_name}")
    print(f"TLE line 1: {satellite_line1}")
    print(f"TLE line 2: {satellite_line2}")

    print("\nSATELLITE POSITION:")

    antenna = Antenna()
    antenna.go_home()

    while True:
        try:
            # Calculate satellite position
            observer.date = datetime.utcnow()
            satellite.compute(observer)

            print(f"Time: {observer.date} - Satellite: {satellite_name} - "
                  f"Azimuth: {satellite.az} - Altitude: {satellite.alt}")

            antenna.set_alt_angle(satellite.alt - 90)
            antenna.set_azi_angle(satellite.az)

            sleep(1)

        except KeyboardInterrupt:
            print("Quitting...")
            exit(0)


if __name__ == "__main__":
    main()
