#!/bin/python3

import requests
import time

import sys
sys.path.append("..")
from src.tracker import Tracker

# Input Observation Site Longitude (Positive Eastward From Greenwich Meridian) and Latitude Coordinates
# Conestoga Campus Year 3 Room By Default
Lat = 43.38747              # Latitude in degrees
Long = 279.60283            # Longitude in degrees (converted to -80.39717)
SatID = 25544               # Enter The Satelite you wish to track here


# ================= Satellite Co-ordinate Retrieval Begins ====================

print('Attempting to retrieve TLE data from the selected satellite...')

response = requests.get(f'https://tle.ivanstanojevic.me/api/tle/{SatID}')

data = response.json()  # This method directly parses the JSON

# Extract data from TLE
tle_line1 = data['line1']
tle_line2 = data['line2']

print('Successfully retrieved orbital data for satellite tracking')

print('Beginning Satellite Tracking')

print('Press the escape key to terminate the program')

tracker = Tracker(Lat, Long, tle_line1, tle_line2)

# ================== Satellite Tracking Loop Begins ====================

try:
    while True:
        azimuth, elevation = tracker.satellite_tracker_setpoints()

        print(f"Observer Azimuth: {azimuth} degrees")
        print(f"Observer Elevation: {elevation} degrees")

        time.sleep(1)  # Wait for 1 second

except KeyboardInterrupt:
    print("Program interrupt detected.")

print("Satellite Tracking Terminated")
