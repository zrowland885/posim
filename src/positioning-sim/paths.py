# -*- coding: utf-8 -*-
""" Path functions to define movement in latiitude and longitude axes """

# SIMPLE PATHS
def stationary(d, _):
    return 0.

def power(d, params):
    if params == None:
        power = 2.
    else:
        power = params['power']
    return d**power

def random(d, params):
    """ Random path """
    import random
    import math
    if params == None:
        b_min = 0.
        b_max = 2*math.pi
    else:
        b_min = params['min']
        b_max = params['max']
    d_noise = random.uniform(b_min, b_max)
    return d_noise


# LINEAR PATH
def linear_lon(d, params):
    import math
    if params == None:
        aziDeg = 45
    else:
        aziDeg = params['aziDeg']
    return d*math.sin(aziDeg*math.pi/180)

def linear_lat(d, params):
    import math
    if params == None:
        aziDeg = 45
    else:
        aziDeg = params['aziDeg']
    return d*math.cos(aziDeg*math.pi/180)

def linear(d, params):
    """ Linear wrapper """
    if params['ordinate'] == 'lat':
        func = linear_lat
    elif params['ordinate'] == 'lon':
        func = linear_lon
    return func(d, params)

def meandering(d, params):
    """ A path that changes direction in increments based on defined input
    lists of distance increments and azimuth angles. Moves linearly."""
    
    splits = params['splits']
    linear_params = {'aziDeg': 45}
    
    for i in range(0, len(splits)-1):
        
        if d >= splits[i] and d < splits[i+1]:
            linear_params['aziDeg'] = params['aziDegs'][i]
            
    if params['ordinate'] == 'lat':
        func = linear_lat
    elif params['ordinate'] == 'lon':
        func = linear_lon
    
    return func(d, linear_params)

def meandering_lat(d, params):
    params['ordinate'] = 'lat'
    return meandering(d, params)

def meandering_lon(d, params):
    params['ordinate'] = 'lon'
    return meandering(d, params)


# TRIGONOMETRIC PATHS
def sine(d, _):
    import math
    return math.sin(d)

def cosine(d, _):
    import math
    return math.sin(d)

def tan(d, _):
    import math
    return math.tan(d)


# CIRCULAR PATH
def circle_sin(d, params):
    """ Sin axis of circle """
    import math
    r = params['radius']
    theta = d/r
    return r*math.sin(theta)

def circle_cos(d, params):
    """ Cos axis of circle """
    import math
    r = params['radius']
    theta = d/r
    return r*math.cos(theta)


# ELLIPTICAL PATH
def ellipse_perimeter(maj_ax, min_ax):
    """ Returns an estimate for the perimeter of an ellipse of semi-major axis
    maj_ax and semi-minor axis min_ax"""
    # https://www.universoformulas.com/matematicas/geometria/perimetro-elipse/
    import math
    H = ((maj_ax - min_ax)/(maj_ax + min_ax))**2
    return math.pi*(maj_ax + min_ax)*(1 + 3*H/(10 + (4 - 3*H)**.5))
    
def ellipse_maj(d, params):
    """ Axis of ellipse aligned with semi-major axis """
    # https://www.mathopenref.com/coordparamellipse.html
    import math
    maj_ax = params['maj_ax']
    min_ax = params['min_ax']
    circ = ellipse_perimeter(maj_ax, min_ax)
    theta = 2*math.pi*d/circ
    return maj_ax*math.sin(theta)

def ellipse_min(d, params):
    """ Axis of ellipse aligned with semi-minor axis """
    # https://www.mathopenref.com/coordparamellipse.html
    import math
    maj_ax = params['maj_ax']
    min_ax = params['min_ax']
    circ = ellipse_perimeter(maj_ax, min_ax)
    theta = 2*math.pi*d/circ
    return min_ax*math.cos(theta)

def ellipse_rotate_maj(d, params):
    """ Axis of rotated ellipse aligned with semi-major axis prior to
    rotation """
    import math
    
    x0 = params['x0']
    y0 = params['y0']
    
    aziDeg = -params['aziDeg']
    aziRad = aziDeg*math.pi/180
    
    ellipse_params = {'maj_ax': params['maj_ax'], 'min_ax': params['min_ax']}
    
    x = ellipse_min(d, ellipse_params)
    y = ellipse_maj(d, ellipse_params)
    
    return math.sin(aziRad)*(x - x0) + math.cos(aziRad)*(y - y0) + x0

def ellipse_rotate_min(d, params):
    """ Axis of rotated ellipse aligned with semi-minor axis prior to
    rotation """
    import math
    
    x0 = params['x0']
    y0 = params['y0']
    
    aziDeg = -params['aziDeg']
    aziRad = aziDeg*math.pi/180
    
    ellipse_params = {'maj_ax': params['maj_ax'], 'min_ax': params['min_ax']}
    
    x = ellipse_min(d, ellipse_params)
    y = ellipse_maj(d, ellipse_params)
    
    return math.cos(aziRad)*(x - x0) - math.sin(aziRad)*(y - y0) + x0


# CUSTOM PATHS
def custom_1(d, _):
    """ Example of custom step path """
    if d < 10:
        return d
    elif d >= 10 and d < 20:
        return d
    elif d >= 20:
        return -d

def custom_2(d, _):
    """ Example of custom step path """
    if d < 10:
        return d**4
    elif d >= 10 and d < 20:
        return d
    elif d >= 20:
        return d
    