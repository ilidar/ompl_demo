#!/usr/bin/env python

import math

class GeodeticPoint(object):
    def __init__(self, lat, lon, alt):
        self.lat = lat
        self.lon = lon
        self.alt = alt

class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

# Geodetic to cartesian convertion
# Reference 1: https://en.wikipedia.org/wiki/Reference_ellipsoid#Coordinates
# Reference 2: https://github.com/purpleskyfall/XYZ2BLH/blob/master/blh2xyz.py

class GeodeticCoordinateSystem(object):
    def __init__(self, origin = GeodeticPoint(0, 0, 0)):
        self.origin = origin

    def convert_to_cartesian(self, geodetic_point):
        A = 6378137.0
        B = 6356752.314245
        latitude = math.radians(geodetic_point.lat)
        longitude = math.radians(geodetic_point.lon)
        height = geodetic_point.alt
        e = math.sqrt(1 - (B**2)/(A**2))
        N = A / math.sqrt(1 - e**2 * math.sin(latitude)**2)
        X = (N + height) * math.cos(latitude) * math.cos(longitude)
        Y = (N + height) * math.cos(latitude) * math.sin(longitude)
        Z = (N * (1 - e**2) + height) * math.sin(latitude)
        return Point(X, Y, Z)

