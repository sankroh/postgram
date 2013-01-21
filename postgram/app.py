#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os
from random import random, choice
from math import sin, cos

from flask import *
import requests

from env import *

app = Flask(__name__)


def get_lat_lng():
    """
    We get a lat/lng point and then pick a point
    within 50KM of it

    Algorithm:
    x,y (cartesian co-ordinates)
    r,Θ (polar co-oridnates)

    Δx = r * cos(Θ)
    Δy = r * sin(Θ)

    x1 = x + Δx
    y1 = y + Δy

    Δlat = x1 - x
    Δlong = y1 - y

    TODO: Verify results with:
    Δσ  = arccos( cos(Δlat) - cos(lat1)*cos(lat2)*(1 - cos(Δlong) )
    """
    multiplier = 10000;
    radius = 50
    # latitude=(random()*(90*multiplier))/multiplier
    # longitude=(random()*(180*multiplier))/multiplier
    latitude = random() * 90
    longitude = random() * 180

    if round(random()*2) == 1:
        latitude*=1
    else:
        latitude*=-1
    if round(random()*2) == 1:
        longitude*=1
    else:
        longitude*=-1

    dx = radius * cos(45)
    dy = radius * sin(45)

    latitude += dx
    longitude += dy

    return latitude,longitude


def get_city_lat_lng():
    """
    Find a random city and return it's lat/lng
    """
    city = choice(city_list)
    return city['lat'], city['lng']


def get_data():
    lat,lng = get_city_lat_lng()
    auth = FOAUTH_USER, FOAUTH_PASSWORD
    data = {'distance': 5000, 'lat': lat, 'lng': lng}
    r = requests.get(FOAUTH_IGRAM_URL, params=data, auth=auth)
    return r, lat, lng


@app.route('/')
def index():
    r, lat, lng = get_data()
    if r.status_code == 200 and len(r.text) > 0:
        resp_dict = json.loads(r.text)
        gurl = '<a href="https://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q={lat}+,+{lng}&vpsrc=0&ie=UTF8&t=m&z=3&iwloc=near">Google Maps</a>'.format(lat=lat,lng=lng)
        try:
            return '<img src="{0}"/><br>{1}<br>{2}<br>{3}'.format(resp_dict['data'][0]['images']['standard_resolution']['url'], resp_dict['data'][0]['location'], resp_dict['data'][0]['link'], gurl)
        except (KeyError, IndexError):
            return str(resp_dict) + str(lat) + ' , ' + str(lng) + '\n\n' + gurl
    else:
        return '{0}-{1}'.format(r.status_code, r.text)


if __name__ == '__main__':
    # Load city list into memory
    f = open('postgram/cities1000.txt', 'r')
    city_list = []
    for line in f.xreadlines():
        city = {}
        line = line.split('\t')
        try:
            city['name'] = line[1]
            city['lat'] = line[4]
            city['lng'] = line[5]
            city_list.append(city)
        except (IndexError, KeyError):
            pass

    f.close()

    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
