"""
    file:
        algorithm.py
    purpose:
        Contains the logic of all the algorithms that numerically analyze route safety metrics
"""

class RatingAlgorithms:
    def __init__(self):
        pass

    def street_light_density(self, routes, lights, verbose=False):
        """
            purpose:
                Calculate the traffic light density per km for each given route
            parameters:
                routes: List of WalkingRoute objects
                lights: List of StreetLight objects
                verbose: optional; default False. If true, function returns all relevant data for debugging
            return:
                density: List of floats that represent lights/pm for each WalkingRoute
                inrange: List of StreetLight objects that were in range of WalkingRoute
                outrange: List of StreetLight objects that were out out range of WalkingRoute

                if verbose, returns (density, inrange, outrange)
                else, returns density
        """

        # List containing sublist of StreetLight objects
        inrange = [[] for _ in routes]

        # List containing sublist of StreetLight objects     
        outrange = [[] for _ in routes]

        # List of light densities
        density = [0] * len(routes)

        for rid, route in enumerate(routes):
            
            # For each route, iterate over all the walking routes
            for light in lights:

                if light.coord.point.within(route.polygon):
                    inrange[rid].append(light)
                else:
                    outrange[rid].append(light)

            # calculate the density of lights based on length of routes and lights in range
            density[rid] = len(inrange[rid]) / route.distance
            
        if not verbose:
            return density
        else:
            return density, inrange, outrange

    # Percentage of path that has sidewalks
    def sidewalk_density(self, routes, sidewalks, verbose=False):
        """
            purpose:
                Calculate the ratio of available sidewalk coverage for each given route
                
                A ratio of 1 means that the entire route has sidewalk coverage on at least one side of the road.
                A ratio <1 means that the route is not entirely covered by sidewalk on at least one side
                A ratio >1 means that the route is covered by sidewalks on one side fully and on both sides some of the time
                A ratio of 2 means that the entire route has sidewalk coverage on both sides
            parameters:
                routes: List of WalkingRoute objects
                sidewalks: List of Sidewalk objects
                verbose: optional; default False. If true, function returns all relevant data for debugging
            return:
                ratio: List of floats that represent lights/pm for each WalkingRoute
                total_len: List of floats that represent the total length of sidewalk in each route
                inrange: List of Sidewalk objects that were in range of WalkingRoute
                outrange: List of Sidewalk objects that were out out range of WalkingRoute

                if verbose, returns (density, inrange, outrange)
                else, returns density
        """

        # Ratio of sidewalk coverage for each route as a float
        ratio = [0] * len(routes)

        # Total length of the sidewalk on each route. Note, the length is not in kilometers but in geometry units based on LAT, LON (not useful)
        total_len = [0] * len(routes)

        # List of sublists of Sidewalk objects that indiciate which sidewalks were in range for what route
        inrange = [[] for _ in routes]

        # List of sublists of Sidewalk objects that indiciate which sidewalks were out of range for what route
        outrange = [[] for _ in routes]

        for rid, route in enumerate(routes):

            # For each route, iterate over all Sidewalk objects
            for sidewalk in sidewalks:
                
                # Check to see if the sidewalk intersects the route at all
                if route.polygon.intersects(sidewalk.line):

                    # Calculate the sidewalk line subsegment that resides within the route polygon
                    sidewalk_in_route = route.polygon.intersection(sidewalk.line)

                    # Track the subsegment
                    inrange[rid].append(sidewalk_in_route)

                    # Accumulate total sidewalk length
                    total_len[rid] += sidewalk_in_route.length

                else:
                    outrange[rid].append(sidewalk.line)
            
            # Ratio calculation; total sidewalk length / total route length
            ratio[rid] = (total_len[rid] / route.line.length)

        if not verbose:
            return ratio
        else:
            return ratio, total_len, inrange, outrange

    def traffic_density(self, routes, roads, verbose=False):
        """
            purpose:
                Calculates the average daily traffic for each route based on the traffic entities
                Simple weighted average calculation
            parameters:
                routes: List of WalkingRoute objects
                sidewalks: List of TrafficVolume objects
                verbose: optional; default False. If true, will also return debugging information
            return:
                avg_volumes: list of floats representing the average traffic per day of each route
                inrange: list of TrafficVolumes that are within range of each route

                if verbose, returns (avg_volumes, inrange)
                else, returns avg_volumes

        """
        
        # Average traffic normalized over the entire route
        avg_volumes = [0] * len(routes)

        # List of sublists of TrafficVolume objects that indiciate which sidewalks were in range for what route
        inrange = [[] for _ in routes]

        for rid, route in enumerate(routes):

            # For each route, iterate over all traffic volumes
            for road in roads:
                
                # Check to see if the road intersects the route at all
                if route.polygon.intersects(road.line):

                    # Calculate the road line subsegment that resides within the route polygon
                    road_in_route = route.polygon.intersection(road.line)

                    inrange.append(road_in_route)

                    # Calculate how much of the route the road covers
                    route_ratio = road_in_route.length / route.line.length

                    # Calculate average volume for road subsegment based on road volume and ratio
                    avg_volumes[rid] += road.volume * route_ratio

        if not verbose:
            return avg_volumes
        else:
            return avg_volumes, inrange