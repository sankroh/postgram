from random import random

def get_lat_long():
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

