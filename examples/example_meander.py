# -*- coding: utf-8 -*-
"""
An example of a randomly moving meandering path.
"""

import random
import numpy as np

import paths
import velocities
import noise
from simulate import Simulation, Character, Plot
from datetime import datetime


def generate_curve_degs(deg_increment, split_len):
    aziDegs = [None]*split_len
    for i in range(0,split_len):
        if i == 0:
            aziDegs[i] = random.uniform(0,359)
        else:
            aziDegs[i] = aziDegs[i-1] + deg_increment
    return(aziDegs)


def generate_meander_degs(meander, split_len):
    aziDegs = [None]*split_len
    for i in range(0,split_len):
        if i == 0:
            aziDegs[i] = random.uniform(0,359)
        else:
            aziDegs[i] = aziDegs[i-1] + random.uniform(-meander,meander)
    return(aziDegs)


#splits = [9*i + x for i, x in enumerate(sorted(random.sample(range(500), 100)))]
splits = np.arange(0,500,1)
split_len = len(splits)

deg_increment = random.uniform(0,359)
meander = random.uniform(-20,20)

# For curve of random radius:
#aziDegs = generate_curve_degs(deg_increment, split_len)
# For meandering path:
aziDegs = generate_meander_degs(meander, split_len)


lat_func_params = {'ordinate':'lat', 'splits': splits, 'aziDegs': aziDegs}
lon_func_params = {'ordinate':'lon', 'splits': splits, 'aziDegs': aziDegs}

# Create character instance
char = Character()
char.lat_func = paths.meandering
char.lat_func_params = lat_func_params
char.lon_func = paths.meandering
char.lon_func_params = lon_func_params

# Create simulation instance
sim = Simulation()
sim.start_time = datetime.strptime('01/01/21 00:00:00', '%d/%m/%y %H:%M:%S')
sim.end_time = datetime.strptime('01/01/21 00:02:00', '%d/%m/%y %H:%M:%S')

# Run threaded
results = sim.run_sim(char)

# Plot results
Plot().plot_combined(results)
