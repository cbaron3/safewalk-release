"""
    file: calculate_rating.py
    purpose: Endpoints for calculating safety ratings based on a start/end point
"""

from flask import request as req
from flask_restful import Resource

from app import gmaps, datapool, algos
from app.metrics.map import max_bounding_box, split_box
from app.endpoints.util import HTTPHandler

import time

class CalcRatingResource(Resource):
    def post(self):
        """
            purpose:
                Get the metrics pertaining to all paths from START to END
            parameters:
                json format [REQUIRED] {
                    start: address for geocoding - str 
                           OR
                           [LAT, LON]

                    end: address for geocoding - str 
                         OR
                         [LAT, LON]

                    debug [optional]: True or False. If true, images of routes are saved in local directory. 
                }
            return:
                HTTP 400 - If no JSON provided
                HTTP 422 - If JSON is formatted improperly
                HTTP 201 - If successful, json = {
                    "status": "success",
                    "data": [
                        {
                            "polyline": str,      Polyline for rendering
                            "lights": float,      Lights per km
                            "sidewalks": float,   Sidewalk availability ratio (Sidewalk distance/route distance)
                            "traffic": float,     Average daily traffic, weighted
                            "duration": float,    Duration of route
                            "distance": float,    Distance of route
                        }, 
                    ]
                }
        """
        
        # Grab JSON data
        print('Hello')
        json_data = req.get_json(force=False)

        print(json_data)        

        if not json_data:
            print('Hello')
            return HTTPHandler.no_data()
            

        # If exception is thrown, JSON is improperly formatted
        try:
            # Grab routes based on start and end
            start = time.time()
            routes = gmaps.walking_routes(json_data['start'], json_data['end'])
            print('To get routes: {}'.format(time.time()-start))

            # Calculate maximum bounding box and split that box into smaller boxes for query
            start = time.time()
            box_ne, box_sw = max_bounding_box(routes)
            boxes = split_box(box_ne, box_sw, 25)
            print('To create boxes: {}'.format(time.time()-start))

            # Collect data from opendata portal
            start = time.time()
            lights, sidewalks, volumes = datapool.collect(boxes)
            print('To collect data: {}'.format(time.time()-start))

            # Calculate metrics
            start = time.time()
            light_density = algos.street_light_density(routes, lights)
            sidewalk_density = algos.sidewalk_density(routes, sidewalks)
            volume_density = algos.traffic_density(routes, volumes)
            print('To run computations: {}'.format(time.time()-start))

            data = []
            for i in range(len(routes)):
                r = 'Route {} has {:.2f} lights/km, {:.2f}% sidewalk availability, and {:.2f} cars per day on average'\
                        .format(i+1, light_density[i], sidewalk_density[i]*100, volume_density[i])
                
                # Format JSON data
                data.append( {"polyline": str(routes[i].polyline),\
                        "lights": light_density[i],\
                        "sidewalks": sidewalk_density[i],\
                        "traffic": volume_density[i],\
                        "duration": routes[i].duration,\
                        "distance": routes[i].distance })

            # Save figure data if debug mode is active
            if json_data.get('debug'):
                if json_data['debug']:
                    import os
                    from config import basedir
                    from datetime import datetime
                    import matplotlib.pyplot as plt

                    # Colors to cycle through for routes
                    colors = ['blue', 'orange', 'pink', 'purple']

                    # Create base directory if needed
                    base_location = basedir + '\plots'
                    if not os.path.exists(base_location):
                        os.mkdir(base_location)

                    # Create directory to save current plots if needed
                    save_location = base_location + r'\{}'.format( datetime.now().strftime("%d_%m_%Y-%H_%M_%S") )
                    if not os.path.exists(save_location):
                        os.mkdir(save_location)

                    # Create figure for street lights
                    plt.figure(figsize=(20,10))

                    # Plot street lights
                    lights = [l.coord.latlng for l in lights]
                    plt.scatter(*zip(*lights), color='grey', s=1)

                    # Plot routes
                    for i in range(len(routes)):
                        x,y = routes[i].polygon.exterior.xy
                        plt.plot(x,y, color=colors[i%4], label='Route {} - {:.2f} lights per km'.format(str(i+1), light_density[i]))

                    # Add legend and save
                    plt.legend(loc="upper left")
                    plt.savefig(save_location + r'\lights.png')

                    # Create figure for sidewalks
                    plt.figure(figsize=(20,10))

                    # Plot sidewalks
                    for sidewalk in sidewalks:
                        x, y = sidewalk.line.xy
                        plt.plot(x, y, color='grey', alpha=0.7, linewidth=1, solid_capstyle='round', zorder=2)

                    # Plot routes
                    for i in range(len(routes)):
                        x,y = routes[i].polygon.exterior.xy
                        plt.plot(x,y, color=colors[i%4], label='Route {} - {:.2f}% sidewalk coverage'.format(str(i+1), sidewalk_density[i]*100))

                    # Add legend and save
                    plt.legend(loc="upper left")
                    plt.savefig(save_location + r'\sidewalks.png')

                    # Create figure for traffic
                    plt.figure(figsize=(20,10))

                    # Assign color codes to different volumes of road
                    for volume in volumes:

                        # Default color
                        c = 'black'
                        if volume.volume > 1000 and volume.volume < 5000:
                            c = 'yellow'
                        elif volume.volume > 5000:
                            c = 'red'
                        else:
                            c = 'green'
                        
                        # Plot the line
                        x, y = volume.line.xy
                        plt.plot(x, y, color=c, alpha=1.0, linewidth=1, solid_capstyle='round', zorder=2)

                    # Plot routes
                    for i in range(len(routes)):
                        x,y = routes[i].polygon.exterior.xy
                        plt.plot(x,y, color=colors[i%4], label='Route {} - {:.2f} average cars per day'.format(str(i+1), volume_density[i]))

                    # Add legend and save
                    plt.legend(loc="upper left")
                    plt.savefig(save_location + r'\traffic.png' )

            return HTTPHandler.valid_data(data)

        except Exception as e:
            print(e)
            return HTTPHandler.improper_data(e)