import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

import seaborn as sns

import matplotlib.pyplot as plt

#import folium
#from folium.plugins import HeatMap
from tqdm import tqdm
import requests
from collections import defaultdict
import numpy as np
import folium

end_lat = 55.757013 

end_lon = 37.631132

def request_routes(start_lat, start_lon, departure_time, key, mode='transit', end_lat=end_lat, end_lon=end_lon):
    
    """Request route from google API"""
    
    url = 'https://maps.googleapis.com/maps/api/directions/json?origin={},{}&mode={}&transit_mode=bus|subway&destination={},{}&departure_time={}&key={}'
    
    url_with_params = url.format(start_lat, start_lon, mode, end_lat, end_lon, departure_time, key)
    
    response = requests.get(url_with_params)
    
    
    return response.json()

def get_transport_access(coords, departure_time, key):
    
	routes = []

	end_lat = 55.757013 

	end_lon = 37.631132

	for coord in tqdm(coords):
	    
	    start_lon = coord[0]
	    start_lat = coord[1]
	    try:
	        route = request_routes(start_lat, start_lon, departure_time, key, 'transit', end_lat, end_lon)
	        routes.append(route['routes'])
	    except:
	        continue
	return routes



def calculateMeasures(routes, origins):

	walking = defaultdict(lambda: [])
	transfers = defaultdict(lambda: [])
	durations = defaultdict(lambda: [])

	for index, route in enumerate(routes):
	    
	    if len(route):
	        originId = origins[index]['id']
	        route = route[0]
	        firstLeg = route['legs'][0]
	        transfers[originId].append(len(firstLeg['steps']) - 1)
	        durations[originId].append(firstLeg['duration']['value'])

	        if len(firstLeg['steps']) == 1:
	            walking[originId].append(firstLeg['steps'][0]['duration']['value']/60.0)
	        else:
	            for step in firstLeg['steps']:
	                if step['travel_mode'] == 'TRANSIT':
	                    break
	                walking[originId].append(step['duration']['value']/60.0)

	walkingMean = [(originId, origins[originId]['lon'], origins[originId]['lat'],
	                 np.mean(dist)) if len(dist) else 0
	                for originId, dist in walking.items()]
	transfersMean = [(originId, origins[originId]['lon'], origins[originId]['lat'],
	                  np.mean(dist)) if len(dist) else 0
	                  for originId, dist in transfers.items()]
	durationsMean = [(originId, origins[originId]['lon'], origins[originId]['lat'],
	                   np.mean(dist)/60.0) if len(dist) else 0
	                  for originId, dist in durations.items()]


	return walkingMean, transfersMean, durationsMean


def get_transport_data(coords, departure_time, key):

	origins = []
	for index, coord in enumerate(coords):
	    origins.append({'lat': coord[1], 'lon': coord[0], 'id': index})

	print("Get routes from google directions API")
	routes = get_transport_access(coords, departure_time, key)

	print("Process routes")

	walkingMean, transfersMean, durationsMean = calculateMeasures(routes,origins)


	walking = pd.DataFrame(walkingMean,
	                   columns=['originId', 'lon', 'lat', 'walking'])
	transfers = pd.DataFrame(transfersMean,
	                         columns=['originId', 'lon', 'lat', 'transfers'])
	duration = pd.DataFrame(durationsMean,
	                        columns=['originId', 'lon', 'lat', 'duration'])
	walking = walking.merge(transfers).merge(duration)

	return walking
