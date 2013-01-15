import json
import os
from random import random

from flask import *
import requests

from env import *

app = Flask(__name__)


def get_lat_lng():
    multiplier = 10000;
    latitude=(random()*(90*multiplier))/multiplier
    longitude=(random()*(180*multiplier))/multiplier
    if round(random()*2) == 1:
        latitude*=1
    else:
        latitude*=-1
    if round(random()*2) == 1:
        longitude*=1
    else:
        longitude*=-1

    return latitude,longitude


def get_data():
    lat,lng = get_lat_lng()
    auth = FOAUTH_USER, FOAUTH_PASSWORD
    data = {'distance': 5000, 'lat': lat, 'lng': lng}
    r = requests.get(FOAUTH_URL, params=data, auth=auth)
    return r


@app.route('/')
def index():
    r = get_data()
    if r.status_code == 200 and len(r.text) > 0:
        resp_dict = json.loads(r.text)
        return str(resp_dict)
    else:
        return ''


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.debug = True
    app.run(host='0.0.0.0', port=port)
