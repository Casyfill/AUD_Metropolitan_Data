import requests as rq
import warnings
import json
from shapely.geometry import shape
import time


def izochrone(coords, apikey, costing="pedestrian", tr_time=15,
              date_time='2016-07-09T00:00', generalize=None, sleep_secs=12):
    ''' request for the izochrone shape from Mapzen

    request for the geojson izochrone shape from Mapzen
    NOTE: for now supports only singlton requests
    check documentation for more information:
    https://mapzen.com/documentation/mobility/isochrone/api-reference/#isochrone-service-api-reference

    Args:
        coords(dict): {lon, lat} float coordinats
        apikey(str): api key, get one here: https://mapzen.com/dashboard
        costing(str): costing mode, one of 'auto', 'bicycle',
                      'pedestrian', 'multimodal'
        tr_time(int): time in minutes
        generalize(float): geometry generalization param, 0 <= x <= 1
        date_time(str): datetime to estimate access
        generalize(float): generalization param (see API documentaiton)
        sleep_secs(int): seconds to sleep for each request. No less than 10!

    Returns:
        shapely.Multypolygon: isochrone

    '''
    base = 'http://matrix.mapzen.com/isochrone'
    sleep_secs = max(11, sleep_secs)  # damage control

    costings = ('auto', 'bicycle', 'pedestrian', 'multimodal')
    if costing not in costings:
        warnings.warn(
            'Costing should be in {0}, got {1} instead. \
             Switching to "pedestrian" mode.'.format(costings, costing))
        costing = "pedestrian"

    print(coords)
    iso_params = json.dumps({"locations": [coords],
                             "costing": costing,
                             "contours": [{'time': tr_time}],
                             'date_time': {'type': 0, 'value': date_time},
                             'polygons': True,
                             'denoise': 1, })

    params = {'json': iso_params,
              'api_key': apikey
              }

    if generalize is not None:
        params['generalize'] = generalize

    result = rq.get(base, params=params)
    if result.status_code != 200:
        print(result.url)

    result.raise_for_status()
    time.sleep(sleep_secs)

    r = [{'geometry': shape(f['geometry']), 'properties':f[
        'properties']} for f in result.json()['features']]
    return r


def turn_by_turn(locations, apikey, costing='multimodal',
                 time_only=True, sleep_secs=12):
    '''return routing between locations



    See info here:
    https://mapzen.com/documentation/mobility/turn-by-turn/api-reference/

    Args:
        locations(list): list of {lat, lon} dictionaries
        apikey(str): api key, get one here: https://mapzen.com/dashboard
        costing(str): costing mode, multimodal by default
        time_only(bool): if return transit time only
        sleep_secs(int): seconds to sleep for each request. No less than 10!
    Returns
        int: transit time in seconds
        OR dict: dictionary, containing all routing information
        '''
    base = 'https://valhalla.mapzen.com/route'
    sleep_secs = max(11, sleep_secs)

    costings = ('auto', 'auto_shorter', 'bicycle', 'bus',
                'hov', 'multimodal', 'pedestrian')

    if costing not in costings:
        warnings.warn('Costing should be one of {0}, got {1} instead.\
                      Setting to "multimodal"'.format(costings, costing))
        costing = 'multimodal'

    request_params = json.dumps({'locations': locations,
                                 'costing': costing,
                                 'directions_options': {
                                     'narrative': False
                                 }
                                 })

    params = {'json': request_params,
              'api_key': apikey
              }

    result = rq.get(base, params=params)
    if result.status_code != 200:
        print(result.url)
    result.raise_for_status()
    time.sleep(sleep_secs)

    if time_only:
        return result.json()['trip']['summary']['time']
    else:
        return result.json()


def geocode(text, apikey, country=None, sleep_secs=12):
    '''forward geocode of the name

    all documentation is here: https://mapzen.com/documentation/search/search/

    text(str): address to search for
    apikey(str): mapzen api key
    country(str): country, to narrow down the search
    sleep_secs(int): number of seconds to sleep after the request

    '''
    base = 'https://search.mapzen.com/v1/search'
    sleep_secs = max(11, sleep_secs)

    params = {'api_key': apikey,
              'text': text}

    if country is not None:
        params['boundary.country'] = country

    result = rq.get(base, params=params)
    if result.status_code != 200:
        print(result.url)

    result.raise_for_status()
    time.sleep(sleep_secs)
    return result.json()  # returns feature_collection
