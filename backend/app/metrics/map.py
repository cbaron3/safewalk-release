"""
    file:
    purpose:
"""

import googlemaps
import polyline

from datetime import datetime
from shapely.geometry import LineString, Point
from app.metrics.util import Coordinate, POLYGON_BUFFER
from math import sqrt

import json
import os
    
class WalkingRoute:
    """
        purpose:
            Simplify Google Maps Walking Route representation; trim the fat
    """

    
    def __init__(self, route_json):
        """
            purpose: 
                Initialize WalkingRoute object based on googlemaps json
            params:
                route_json: Googlemap's walking route api response
        """

        self.ne_corner = Coordinate(route_json['bounds']['northeast']['lat'], route_json['bounds']['northeast']['lng'])
        self.sw_corner = Coordinate(route_json['bounds']['southwest']['lat'], route_json['bounds']['southwest']['lng'])

        # TODO: Distance text not reliable. Specify unit and use value instead. See https://developers.google.com/maps/documentation/directions/intro
        self.distance = float(route_json['legs'][0]['distance']['text'].split(' ')[0])

        self.duration = float(route_json['legs'][0]['duration']['value'])
        
        if route_json['legs'][0]['distance']['text'].split(' ')[1] == 'mi':
            self.distance *= 1.60934 # Convert mi to km

        self.polyline = route_json['overview_polyline']['points']

        self.points = polyline.decode(self.polyline)

        waypoints = [(w[1], w[0]) for w in self.points]
        self.line = LineString(waypoints)

        self.polygon = self.line.buffer(POLYGON_BUFFER)
    
    def equals(self, other):
        """
            purpose:
                Because WalkingRoute's cannot be uniquely identified by an ID, compare routes based on polyline
            param:
                other: WalkingRoute to compare self too
        """

        try:
            if self.polyline == other.polyline:
                return True
            else:
                return False
        # If exception is tossed, other does not have a data element called 'polyline'
        except:
            return False

    def to_json(self):
        elem = {
            'ne_corner': self.ne_corner.latlng,
            'sw_corner': self.sw_corner.latlng,
            'distance': self.distance,
            'polyline': self.polyline,
        }

        return json.loads(elem)

    def __str__(self):
        return '{} km walking route'.format(self.distance)
    
    def __repr__(self):
        return '{} km walking route'.format(self.distance)

def max_bounding_box(routes):
    """
        purpose:
            Compute the ne and sw corners of the box that encompasses all WalkingRoutes
        params:
            routes: List of WalkingRoute objects
        return:
            (ne, sw): corners of the bounding box that surrounds the bounding boxes for all the routes
    """

    # Assume first route is the box
    max_ne = Coordinate(*routes[0].ne_corner.latlng)
    max_sw = Coordinate(*routes[0].sw_corner.latlng)

    # ONLY VALID FOR WEST HEMISPHERE, NORTH HEMISPHERE
    # ne_bound will be the largest lat and the largest lon (closest to 0)
    # sw_bound will be the smallest lat and the smallest lon
        
    for route in routes:
        max_ne.lat = max(max_ne.lat, route.ne_corner.lat)   # LAT
        max_ne.lon = min(max_ne.lon, route.ne_corner.lon)

        max_sw.lat = min(max_sw.lat, route.sw_corner.lat)
        max_sw.lon = min(max_sw.lon, route.sw_corner.lon)

    return max_ne, max_sw 

def split_box(ne, sw, box_count):
    """
        purpose:
            Take a bounding box dictated by the ne and sw corners and split it into a list of equally sized sub boxes
        params:
            ne: Coordinate for ne corner
            sw: Coordinate for sw corner
            box_count: Number of sub boxes to create; must be a square number
        return:
            boxes: List of (Coordinate, Coordinate) where the first coordinate is the SW corner and the second is the NE corner
    """
    # Boxes has to be 4, 9, 16 ... Assert on sqrt

    # TopLeft    TopRight
    # BottomLeft BottomRight
    top_left = Coordinate(ne.lat, sw. lon)
    bottom_right = Coordinate(sw.lat, ne.lon)
    top_right = ne
    bottom_left = sw

    # Convert bottom left coords to int with scalar so they can be iterated upon
    lon0 = int(bottom_left.lon * 1000000)
    lon2 = int(bottom_right.lon * 1000000)

    lat0 =  int(bottom_left.lat * 1000000)
    lat1 = int(top_left.lat * 1000000)

    # Calculate range between min and max lat, min and max lon
    total_lat = lat1 - lat0
    total_lon = lon2 - lon0

    delta_lat = int( (total_lat/sqrt(box_count)))
    delta_lon = int( (total_lon/sqrt(box_count)))
    
    boxes = []

    # Loop over rows and columns of lat/lon corners
    for i in range(lon0, lon2, delta_lon):
        for j in range(lat0, lat1, delta_lat):

            # Convert back from int to float and calculate corner locations
            f_i = float(i/1000000)
            f_j = float(j/1000000)
            f_di = float(delta_lon/1000000)
            f_dj = float(delta_lat/1000000)

            # Determine corner coordinates
            ne_ = f_j , f_i
            sw_ = f_j + f_dj, f_i + f_di

            boxes.append((Coordinate(*sw_), Coordinate(*ne_)))

    return boxes

class GMapsAPI:
    def __init__(self, key):
      self.key = key

    def create_conn(self):
        """
            purpose:
                Creates a connection with the Google Maps API based on the Object's key
            return
                True if connection was successful, else False. 
        """
        try:
            self.gmaps = googlemaps.Client(self.key)
            return True
        except Exception as e:
            print(e)
            return False

    
    def walking_routes(self, from_loc, to_loc):
        """
            purpose: 
                Query Google Maps API for walking directions based on from/to locations
            parameters:
                from_loc - Start location
                to_loc - End Location

                Locations are either (LON [float], LAT [float]) in decimal degrees or ADDRESS [str]. 
                When ADDRESS is supplied, Google Maps geocode service is called, extra API call
            return:
                Returns list of WalkingRoute objects or None if error occured
        """

        # When the type of both input arguments are strings, attempt to geocode the addresses
        if type(to_loc) == str:
            try:
                to_loc = self.gmaps.geocode(to_loc)
                to_loc = (to_loc[0]['geometry']['location']['lat'], to_loc[0]['geometry']['location']['lng'])
                
            except Exception as e:
                print('String parameters could not be geocoded: {}'.format(e))

        if type(from_loc) == str:
            try:
                from_loc = self.gmaps.geocode(from_loc) 
                from_loc = (from_loc[0]['geometry']['location']['lat'], from_loc[0]['geometry']['location']['lng'])

            except Exception as e:
                print('String parameters could not be geocoded: {}'.format(e))

        # Query Maps API with FROM_LOC and TO_LOC
        try:
            routes = self.gmaps.directions(origin=tuple(from_loc),
                                destination=tuple(to_loc),
                                mode="walking",
                                alternatives=True,
                                units="metric",      # Get as many routes as possible
                                departure_time=datetime.now())

            unpacked_routes = [WalkingRoute(route) for route in routes]

            return unpacked_routes

        except Exception as e:
           print('Failed to find route: {}'.format(e))

if __name__ == "__main__":
    START = '1673 Richmond St', (43.025454, -81.283798)
    END = '3020 Gore Rd', (42.988210, -81.140668)

    maps = GMapsAPI(os.getenv('FLASK_APP_BACKEND_GMAPS_API_KEY'))
    status = maps.create_conn()

    if not status:
        print('Maps API failed to connect')
    else:
        print("Maps API successfully connected")

    result = maps.walking_routes(START[0], END[0])
    print(result)

    result = maps.walking_routes(START[1], END[1])
    print(result)
