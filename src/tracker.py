from sgp4.api import Satrec, jday
from datetime import datetime, timezone
from math import floor
import numpy as np
import math

# Universal TLE Satellite Tracking Algorithm
# Written by Brandon Hauck
# Using Equations & Algorithms from Orbital Mechanics for Engineering Students by Howard Curtis
# Azimuth and Elevation Calculation utilizes methods From Alfred Bencomo's ISSOT Project


class Tracker():
    def __init__(self, lat, long, tle1, tle2):
        self.lat = lat
        self.long = long
        self.tle1 = tle1
        self.tle2 = tle2

        # Initialize satellite record from TLE data
        self.satellite = Satrec.twoline2rv(self.tle1, self.tle2)

    def zero_to_360(self, degrees):
        """
        Reduces an angle to the range 0 - 360 degrees.
        """
        if degrees >= 360:
            degrees = degrees - floor(degrees / 360) * 360
        elif degrees < 0:
            degrees = degrees - (floor(degrees / 360) - 1) * 360
        return degrees

    def LST(self, jd, hour, minute, seconds, EL):
        """
        This Function utilizes the example algorithm in Orbital Mechanics for Engineering Students by Howard Curtis 
        Page 623 relating to Chapter 5.3 Example 5.06
        Purpose: Calculates the Local Sidereal Time using EL the locations East Longitude.
        """
        # Julian day number at 0 hr UT
        j0 = jd

        # Number of centuries since J2000
        j = (j0 - 2451545) / 36525

        # Greenwich sidereal time (degrees) at 0 hr UT
        g0 = 100.4606184 + 36000.77004 * j + 0.000387933 * j**2 - 2.583e-8 * j**3
        g0 = self.zero_to_360(g0)

        # Convert current time to UT
        ut = hour + minute / 60 + seconds / 3600

        # Greenwich sidereal time (degrees) at the specified UT
        gst = g0 + 360.98564724 * ut / 24

        # Local sidereal time
        lst = gst + EL

        # Reduce lst to the range 0 - 360 degrees
        lst = lst - 360 * floor(lst / 360)
        return lst

    def eci_to_ecef(self, eci_coords, gst_angle_degrees):

        """
        Converts earths central inertial frame (fixed celestially) to earth centered earth fixed (rotates with earth, fixed surface)
        """

       # Convert GST (Greenwich Sidereal Time | LST when EL = 0) from degrees to radians
        gst_angle_radians = np.radians(gst_angle_degrees)

        # Create the rotation matrix around the Z-axis
        rotation_matrix = np.array([
            [np.cos(gst_angle_radians), np.sin(gst_angle_radians), 0],
            [-np.sin(gst_angle_radians), np.cos(gst_angle_radians), 0],
            [0, 0, 1]
        ])

        # Perform the rotation using the supplied SGP4 position vector
        ecef_coords = rotation_matrix.dot(eci_coords)

        return ecef_coords

    def calculate_position_vectors(self, position_vector, Gst):

        # This function utilizes formulas and methods available for referrence in the textbook
        # Orbital Mechanics for Engineering Students by Howard Curtis on page 155 of Chapter 4.3 Example 4.1

        # Convert ECI to ECEF for satellite ground tracking
        position_vector = self.eci_to_ecef(position_vector, Gst)

        # Calculate the current magnitude of the satellites resultant position vector (r)
        r_magnitude = np.linalg.norm(position_vector)

        # Calculate the satellites current unit vector (u_r)
        unit_vector = position_vector / r_magnitude if r_magnitude != 0 else np.zeros_like(position_vector)

        # Calculate the satellites current declination (latitude) in degrees
        declination = np.degrees(np.arcsin(unit_vector[2]))

        # Convert declination back to radians for calculating the cosine
        cos_declination = np.cos(np.radians(declination))

        # Calculate cos(alpha) and sin(alpha) using the provided equations
        cos_alpha = np.arccos((unit_vector[0] / cos_declination))
        sin_alpha = np.arcsin((unit_vector[1] / cos_declination))

        # Determine alpha (longitude) in radians
        # Arccos will return the principal value (0 to pi radians), so we adjust to the third quadrant
        alpha = cos_alpha if sin_alpha >= 0 else 2 * np.pi - cos_alpha

        # Convert alpha to degrees
        alpha = np.degrees(alpha)

        r_ascension = (alpha)

        if r_ascension > 180:
            longitude = r_ascension - 360
        else:
            longitude = r_ascension

        return declination, longitude, position_vector

    def satellite_tracker_setpoints(self):
        f = 0.00329                 # Flattening factor of earth
        Re = 6378                   # Earth's Radius at the equator (km)

        # ================== Satellite Co-ordinate Retrieval Begins =====================

        # Get the current date and time
        now = datetime.now(timezone.utc)

        # Convert the current date and time to Julian date and fraction
        jd, fr = jday(now.year, now.month, now.day, now.hour, now.minute, now.second + now.microsecond * 1e-6)

        # Calculate LST for accurate Satellite Longitude Tracking (SGP4 Uses ECIF, Need to convert to ECEF)
        Gst = self.LST(jd, now.hour, now.minute, now.second + now.microsecond * 1e-6, 0)

        # Get the position and velocity of the satellite at the supplied epoch time from SGP4 (Simplified Perturbations Models)  
        e, r, v = self.satellite.sgp4(jd, fr)

        declination, longitude, ECEF_r = self.calculate_position_vectors(r, Gst)

        if e != 0:

            print("Error predicting the satellite's current position and velocity")

        #============== Topocentric Satellite Tracking Algorithm Begins =============

        # This algorithm utilizes Azimuth and Elevation Calculations Altered From Alfred Bencomo's ISSOT Project 
        # https://ieiuniumlux.github.io/ISSOT/
        # This algorithm will generate accurate Azimuth and Elevation setpoints for satellite tracking
        # Provided the base of the tracking system is calibrated for True North = 0 degrees, NE 90, S 180, NW 270
        # The Elavation pitch of the tracking system should represent Horizon = 0 degrees, zenith = 90 degrees (Observers True vertical)
        # Any Negative Elevation angles represent objects that are below the local horizon and cannot be tracked by elevation

        # The expression inside the atan2 function uses spherical trigonometry to account for the curvature of the Earth and provides 
        # the angle in radians from the north direction to the point where the satellite appears on the horizon. 
        # This formula is a simple and accurate calculation which considers the spherical nature of the Earth, as well as the specific 
        # positions of both the satellite and the ground station.

        # Convert degrees to radians
        phi1 = math.radians(self.lat)           # Phi1       -   Groundstation lattitude
        lambda1 = math.radians(self.long)       # Lambda1    -   Groundstation longitude
        phi2 = math.radians(declination)   # Phi2       -   lattitude value of the satellites groundtrack location
        Lambda2 = math.radians(longitude)  # Lambda2    -   longitude value of the satellites groundtrack location

        # change in lambda represents the difference in longitude between the satellite and the ground station

        # Calculate azimuth from the observers true north in the clockwise direction to the satellites location 
        psi = math.degrees(math.atan2(math.sin(Lambda2 - lambda1) * math.cos(phi2), math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(Lambda2 - lambda1)))

        # Ensure azimuth is always between 0 and 360 degrees
        psi = psi % 360

        # Calculate the earth central angle of the satellite to the ground station
        gamma = math.acos(math.sin(phi1) * math.sin(phi2) + math.cos(phi1) * math.cos(phi2) * math.cos(lambda1 - Lambda2))

        # Approximate Re due to earths oblateness from Observation Sites Lattitude
        Re_El = Re - ((Re * f) * (self.lat / 90))

        # Calculate the distance of the Satellite to the center of the earth
        rS = np.linalg.norm(ECEF_r)

        # Calculate the distance to the Satellite from the observation station
        d = math.sqrt((1 + (Re_El / rS)**2) - (2 * (Re_El / rS) * math.cos(gamma)))

        # Calculate the elevation angle
        El = math.degrees(math.acos(math.sin(gamma) / d)) * (-1 if d > 0.34 else 1)

        return psi, El
