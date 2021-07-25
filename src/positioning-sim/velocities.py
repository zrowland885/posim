# -*- coding: utf-8 -*-
""" Velocity functions to define movement speed and direction """

def random(t, params):
    """ Random velocity """
    import random
    if params == None:
        b_min = 0.1
        b_max = 1.0
    else:
        b_min = params['min']
        b_max = params['max']
    velocity = random.uniform(b_min, b_max)
    return velocity

def stationary(t, _):
    return 0.

def fixed(t, params):
    return params['velocity']
