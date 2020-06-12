"""
    file:
        opendata.py
    purpose:
        Contains the logic of interacing with the London OpenData API including organizing data elements
"""

import requests
import json

from shapely.geometry import LineString, Point
from app.metrics.map import WalkingRoute

from math import sqrt

from threading import Thread
from app.metrics.util import Coordinate, POLYGON_BUFFER

class StreetLight:
    """
        purpose:
            Define a StreetLight object
        properties:
            ID - Unique ID provided by OpenData
            coord - Coordinate
    """
    def __init__(self, light_json):
        """
            purpose:
                Construct StreetLight object
            parameters:
                light_json - JSON representing the features of a single Streetlight returned by the OpenData API
        """

        # Extract ID
        self.id = light_json["attributes"]["OBJECTID"]

        # Create coordinate
        self.coord = Coordinate(light_json["geometry"]["x"], light_json["geometry"]["y"])

    # String format    
    def __str__(self):
        return 'ID: {} - {},{}'.format(self.id, self.coord.lat, self.coord.lon)

    # Representative format    
    def __repr__(self):
        return 'LightPoint( ID: {} - {}, {} )'.format(self.id, self.coord.lat, self.coord.lon)

class Sidewalk:
    """
        purpose:
            Define a Sidewalk object
        parameters:
            ID - Unique ID provided by OpenData
            length - Length of sidewalk segment in KM
            points - List of coordinates that represent the path of the sidewalk
            line - LineString element used for plotted
    """

    def __init__(self, sidewalk_json):
        # Extract ID
        self.id = sidewalk_json["attributes"]["OBJECTID"]
        
        # Get length and convert it to kilometers
        self.length = sidewalk_json["attributes"]["Shape.STLength()"] / 1000

        # Extract points on sidewalk path
        points = sidewalk_json["geometry"]["paths"][0]

        # List of coordinates
        self.points = [Coordinate(point[0], point[1]) for point in points]

        # LineString based on list of points
        self.line = LineString([(point[0], point[1]) for point in points])

        self.polygon = self.line.buffer(POLYGON_BUFFER)

    # String format    
    def __str__(self):
        return 'ID: {} Length: {}'.format(self.id, self.length)
    
    # Representative format   
    def __repr__(self):
        return 'Sidewalk ID: {} Length: {}'.format(self.id, self.length)

class TrafficVolume:
    """
        purpose:
            Define a Sidewalk object
        parameters:
            ID - Unique ID provided by OpenData
            volume - Average annual daily traffic volume in # of cars
            length - Length of sidewalk segment in KM
            points - List of coordinates that represent the path of the sidewalk
            line - LineString element used for plotted
    """
    
    def __init__(self, volume_json):
        # Extract ID
        self.id = volume_json["attributes"]["OBJECTID"]
        
        # Get length and convert it to kilometers
        self.length = volume_json["attributes"]["Shape.STLength()"] / 1000

        # Get volume of traffic
        self.volume = volume_json["attributes"]["VolumeCount"]

        # Extract points on sidewalk path
        points = volume_json["geometry"]["paths"][0]

        # List of coordinates
        self.points = [Coordinate(point[0], point[1]) for point in points]

        # LineString based on list of points
        self.line = LineString([(point[0], point[1]) for point in points])

        self.polygon = self.line.buffer(POLYGON_BUFFER)

    # String format    
    def __str__(self):
        return 'ID: {} Length: {}, Average Volume: {}'.format(self.id, self.length, self.volume)
    
    # Representative format   
    def __repr__(self):
        return 'TrafficVolume ID: {} Length: {}, Average Volume: {}'.format(self.id, self.length, self.volume)

class OpenDataLondon:
    """
        purpose:
            Handle London OpenData API calls
    """

    def __init__(self):
        pass

    def __bounding_box_route(self, along_route: WalkingRoute):
        """
            purpose:
                Create the API endpoint string based on the bounding box around a WalkingRoute
            parameters:
                along_route: WalkingRoute object that defines bounding box
            return:
                geometry: string representing API url with bounding box around route
        """

        # Requires LON, LAT but google maps is LAT, LON
        box_ne = '{}%2C{}'.format(along_route.ne_corner.latlng[1], along_route.ne_corner.latlng[0])
        box_sw = '{}%2C{}'.format(along_route.sw_corner.latlng[1], along_route.sw_corner.latlng[0])

        geometry = '&geometry={}%2C{}&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects'.format(box_ne, box_sw)

        return geometry

    def __bounding_box(self, ne, sw):
        """
            purpose:
                Create the API endpoint string based on the bounding box defined by the northeast and southwest coordinates
            parameters:
                ne: Northeast Coordinate object
                sw: Southwest Coordinate object
            return:
                geometry: string representing API url with bounding box around coordinates
        """

        # Requires LON, LAT but google maps is LAT, LON
        box_ne = '{}%2C{}'.format(ne.lon, ne.lat)
        box_sw = '{}%2C{}'.format(sw.lon, sw.lat)

        geometry = '&geometry={}%2C{}&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects'.format(box_ne, box_sw)

        return geometry

    def get_street_lights_onroute(self, along_route : WalkingRoute):
        """
            purpose:
                Get all street lights along WalkingRoute
            parameters:
                along_route: WalkingRoute object
            return:
                street_lights: List of StreetLight objects that are within the bounds of the route
        """

        # Base URL
        geometry = self.__bounding_box_route(along_route)
        url = 'https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=Shape,OBJECTID{}&outSR=4326&f=json'.format(geometry)

        api_result = requests.get(url)
        api_response = json.loads(api_result.text)

        street_lights = [StreetLight(element) for element in api_response['features']]

        return street_lights

    def get_street_lights_inbox(self, ne_corner, sw_corner):
        """
            purpose:
                Get all street lights within a bounding box
            parameters:
                ne_corner: Northeast Coordinate object
                sw_corner: Southwest Coordinate object
            return:
                street_lights: List of StreetLight objects that are within the bounds of the box
        """
        
        # Base URL
        geometry = self.__bounding_box(ne_corner, sw_corner)
        url = 'https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/19/query?where=1%3D1&outFields=Shape,OBJECTID{}&outSR=4326&f=json'.format(geometry)

        api_result = requests.get(url)
        api_response = json.loads(api_result.text)

        street_lights = [StreetLight(element) for element in api_response['features']]

        return street_lights

    def get_sidewalks_onroute(self, along_route : WalkingRoute):
        """
            purpose:
                Get all sidewalk data along WalkingRoute
            parameters:
                along_route: WalkingRoute object
            return:
                sidewalks: List of Sidewalk objects that are within the bounds of the route
        """

        # Base URL
        geometry = self.__bounding_box_route(along_route)
        url = 'https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/4/query?where=1%3D1&outFields=OBJECTID,Shape.STLength(){}&outSR=4326&f=json'.format(geometry)

        api_result = requests.get(url)
        api_response = json.loads(api_result.text)

        sidewalks = [Sidewalk(element) for element in api_response['features']]

        return sidewalks
    
    def get_sidewalks_inbox(self, ne_corner, sw_corner):
        """
            purpose:
                Get all sidewalk data within a bounding box
            parameters:
                ne_corner: Northeast Coordinate object
                sw_corner: Southwest Coordinate object
            return:
                street_lights: List of Sidewalk objects that are within the bounds of the box
        """

        # Base URL
        geometry = self.__bounding_box(ne_corner, sw_corner)
        url = 'https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/4/query?where=1%3D1&outFields=OBJECTID,Shape.STLength(){}&outSR=4326&f=json'.format(geometry)

        api_result = requests.get(url)
        api_response = json.loads(api_result.text)

        sidewalks = [Sidewalk(element) for element in api_response['features']]

        return sidewalks

    def get_traffic_volumes_onroute(self, along_route : WalkingRoute):
        """
            purpose:
                Get all traffic volume data along WalkingRoute
            parameters:
                along_route: WalkingRoute object
            return:
                volumes: List of TrafficVolume objects that are within the bounds of the route
        """

        # Base URL
        geometry = self.__bounding_box_route(along_route)
        url = 'https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/21/query?where=1%3D1&outFields=OBJECTID,Shape.STLength(),VolumeCount{}&outSR=4326&f=json'.format(geometry)

        api_result = requests.get(url)
        api_response = json.loads(api_result.text)

        volumes = [TrafficVolume(element) for element in api_response['features']]

        return volumes

    def get_traffic_volumes_inbox(self, ne_corner, sw_corner):
        """
            purpose:
                Get all traffic volume data within a bounding box
            parameters:
                ne_corner: Northeast Coordinate object
                sw_corner: Southwest Coordinate object
            return:
                street_lights: List of TrafficVolume objects that are within the bounds of the box
        """

       # Base URL
        geometry = self.__bounding_box(ne_corner, sw_corner)
        url = 'https://maps.london.ca/arcgisa/rest/services/OpenData/OpenData_Transportation/MapServer/21/query?where=1%3D1&outFields=OBJECTID,Shape.STLength(),VolumeCount{}&outSR=4326&f=json'.format(geometry)

        api_result = requests.get(url)
        api_response = json.loads(api_result.text)

        volumes = [TrafficVolume(element) for element in api_response['features']]

        return volumes

class DataThreadPool:
    """
        purpose:
            Streamline interact with OpenData helper class. Automatically multithreads API call
            to avoid hitting the maximum API request limit.
    """
    def __init__(self):
        self.data_source = OpenDataLondon()

    def __uniques(self,iterable):
        """
            purpose: 
                Remove non-unique elements (determined by ID) from iterable
            parameters:
                iterable: container
            return:
                uniques: original iterable but with only unique elements
        """

        # Return only the unique elements in the iterable container
        seen = set()
        uniques = []

        for i in iterable:
            if i.id not in seen:
                seen.add(i.id)
                uniques.append(i)

        return uniques

    def __flatten(self, iterable):
        """
            purpose:
                Flatten list of lists
            parameters:
                iterable: list of lists
            return:
                single list
        """

        # Convert a list of lists into one list
        return [item for sublist in iterable for item in sublist]

    def collect(self, boxes):
        """
            purpose:
                Split the process of collecting relevant data from the OpenData API into multiple threads
                to avoid running into the 1000 element request limit. Threaded approach chosen so each API
                call does not need to be made sequentially
            params:
                boxes = list of boxes that defines the API query area. Through testing, 25 or 36 boxes is a good number for entire city
            returns:
                ( list(StreetLight), list(Sidewalk), list(TrafficVolume) )
        """

        # Through testing, it seems like this is the best number of threads to avoid having too many boxes being handled by each thread
        # which will ensure API request limits are not met
        nthreads = int(sqrt(len(boxes)))

        # Containers for thread data, by reference
        lights = []
        sidewalks = []
        volumes = []

        threads = []

        # Split long list of boxes into smaller chucks so each thread only takes on some boxes; not all
        for i in range(nthreads):
            sub_boxes = boxes[i::nthreads]

            t_l = Thread(target=self.__process_lights, args=(sub_boxes,lights))
            t_s = Thread(target=self.__process_sidewalks, args=(sub_boxes,sidewalks))
            t_v = Thread(target=self.__process_volumes, args=(sub_boxes,volumes))

            # Append thread ids
            threads.append(t_l)
            threads.append(t_s)
            threads.append(t_v)

        # Start threads
        [ t.start() for t in threads ]
        # Wait for the threads to finish
        [ t.join() for t in threads ]
        
        # Flatten sub lists cause each thread returns a list
        lights = self.__flatten(lights)
        sidewalks = self.__flatten(sidewalks)
        volumes = self.__flatten(volumes)

        # Remove duplicates in case bounding boxes overlap
        lights = self.__uniques(lights)
        sidewalks = self.__uniques(sidewalks)
        volumes = self.__uniques(volumes)

        return lights, sidewalks, volumes
        
    def __process_lights(self, boxes, container):
        """
            purpose:
                Thread target; get street light data for each box
            parameters:
                boxes: bounding boxes for query
                container: to store results in
            return:
                container: updated container after adding lights 
        """

        for box in boxes:
            # Unpack tuple of coordinates
            container.append( self.data_source.get_street_lights_inbox(*box) )
        return container

    def __process_sidewalks(self, boxes, container):
        """
            purpose:
                Thread target; get sidewalk data for each box
            parameters:
                boxes: bounding boxes for query
                container: to store results in
            return:
                container: updated container after adding sidewalk data 
        """

        for box in boxes:
            # Unpack tuple of coordinates
            container.append( self.data_source.get_sidewalks_inbox(*box) )
        return container

    def __process_volumes(self, boxes, container):
        """
            purpose:
                Thread target; get traffic volume data for each box
            parameters:
                boxes: bounding boxes for query
                container: to store results in
            return:
                container: updated container after adding traffic volume data
        """
        
        for box in boxes:
            # Unpack tuple of coordinates
            container.append( self.data_source.get_traffic_volumes_inbox(*box) )
        return container