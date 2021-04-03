# -*- coding: utf-8 -*-
"""
"""

import paths
import velocities
from simulate import Simulation, Character, Plot
from datetime import datetime

char1 = Character()
char1.name = 'char1'
char1.velocity_func = velocities.random
char1.lat_func = paths.linear
char1.lat_func_params = {'ordinate': 'lat', 'aziDeg': 90}
char1.lon_func = paths.linear
char1.lon_func_params = {'ordinate': 'lon', 'aziDeg': 90}

char2 = Character()
char2.name = 'char2'
char2.start_pos = (0.001,0.)

char3 = Character()
char3.name = 'char3'
ellipse_rotate_params = {'x0': 0., 'y0': 0., 'aziDeg': 45, 'maj_ax': 100., 'min_ax': 20.}
char3.lat_func = paths.ellipse_rotate_maj
char3.lon_func = paths.ellipse_rotate_min
char3.lat_func_params = ellipse_rotate_params
char3.lon_func_params = ellipse_rotate_params

sim = Simulation()

sim.start_time = datetime.strptime('13/03/21 00:00:00', '%d/%m/%y %H:%M:%S')
sim.end_time = datetime.strptime('13/03/21 00:04:16', '%d/%m/%y %H:%M:%S')

results = sim.run_threaded([char1, char2, char3])

Plot().plot_combined(results)
