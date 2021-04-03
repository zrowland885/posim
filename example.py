# -*- coding: utf-8 -*-
"""
An example simulation of three different characters moving in different paths.
"""

import paths
import velocities
import noise
from simulate import Simulation, Character, Plot
from datetime import datetime

# Create char1 instance: linear path with noise
char1 = Character()
char1.name = 'char1'
char1.lat_func = paths.linear
char1.lat_func_params = {'ordinate': 'lat', 'aziDeg': 60}
char1.lon_func = paths.linear
char1.lon_func_params = {'ordinate': 'lon', 'aziDeg': 60}
char1.lat_noise = noise.random
char1.lon_noise = noise.random
char1_noise_params = {'min': -1., 'max': 3.}
char1.lat_noise_params = char1_noise_params
char1.lon_noise_params = char1_noise_params

# Create char2 instance: path starting from a different point
char2 = Character()
char2.name = 'char2'
char2.start_pos = (0.001,0.)

# Create char3 instance: elliptical path with randomised velocity
char3 = Character()
char3.name = 'char3'
ellipse_rotate_params = {'x0': 0., 'y0': 0., 'aziDeg': 45, 'maj_ax': 100., 'min_ax': 20.}
char3.lat_func = paths.ellipse_rotate_maj
char3.lon_func = paths.ellipse_rotate_min
char3.lat_func_params = ellipse_rotate_params
char3.lon_func_params = ellipse_rotate_params
char3.velocity_func = velocities.random

# Create simulation instance
sim = Simulation()
sim.start_time = datetime.strptime('01/01/21 00:00:00', '%d/%m/%y %H:%M:%S')
sim.end_time = datetime.strptime('01/01/21 00:02:00', '%d/%m/%y %H:%M:%S')

# Run threaded
results = sim.run_threaded([char1, char2, char3])

# Plot results
Plot().plot_combined(results)
