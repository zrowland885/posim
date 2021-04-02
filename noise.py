# -*- coding: utf-8 -*-
""" Noise functions to distort movement in latitude and longitude axes """

def no_noise(o, _):
    return o

def random(o, params):
    """ Random noise """
    import random
    if params == None:
        b_min = 0.5
        b_max = 1.5
    else:
        b_min = params['min']
        b_max = params['max']
    o_noise = o*random.uniform(b_min, b_max)
    return o_noise

def drift(o, params):
    """ Linearly drift movement in axis over time """
    if params == None:
        drift = .1
    else:
        drift = params['shift']
    return o + drift
