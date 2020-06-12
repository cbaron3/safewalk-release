"""
    file: util.py
    purpose: Encapsulate utility functions for the metrics module
"""

from shapely.geometry import Point

# Global variable used to keep a constant buffer across all polygons
POLYGON_BUFFER = 0.00025

class Coordinate:
    """
        purpose: Define a coordinate
    """

    def __init__(self, x, y):
        """
            parameters: 
                x - x-value of coordinate; Latitude in geocentric
                y - y-value of coordinate; Latitude in geocentric
        """
        
        self.lat = x
        self.lon = y

        # Shapely Point object
        self.point = Point(self.lat, self.lon) # Standard is LAT = y, LON = x

        self.latlng = (self.lat, self.lon)
        self.lnglat = (self.lon, self.lat)