# -*- coding: utf-8 -*-
"""
An example of converting a list of coordinates to a linear path function, then
simulating the path with some noise.
"""

import noise
from convert import coords2path
from simulate import Simulation, Character, Plot
from datetime import datetime

# Coordinates that roughly trace the Pyg and Llanberis path up Mt. Snowdon
snowdon_pyg_wgs84 = [
    (53.080225, -4.020847),
    (53.078237, -4.040373),
    (53.076977, -4.041660),
    (53.072404, -4.054320),
    (53.072212, -4.061455),
    (53.073733, -4.063547),
    (53.072763, -4.077216),
    (53.073356, -4.076379),
    (53.072724, -4.079641),
    (53.068509, -4.076498)
    ]

# Reviewing the function strings can be useful for debugging
latf, lonf, latfstr, lonfstr = coords2path(snowdon_pyg_wgs84)

# Create a character instance with some noise
char = Character()
char.lat_func = latf
char.lon_func = lonf
char.lat_noise = noise.random
char.lon_noise = noise.random
noise_params = {'min': 0., 'max': 2.}
char.lat_noise_params = noise_params
char.lon_noise_params = noise_params

# Create the simulation
# The route takes about 1:20 hrs at 1 m/s. According to google maps it should
# take 1:24 hrs so this makes sense. To avoid the southward movement that
# occurs after reaching the summit, assign a velocity function to the
# Character that returns 0 after 4933 m (distance to the peak - see function
# strings).
sim = Simulation()
sim.start_time = datetime.strptime('01/01/21 00:00:00', '%d/%m/%y %H:%M:%S')
sim.end_time = datetime.strptime('01/01/21 01:20:00', '%d/%m/%y %H:%M:%S')
sim.timestep = 30

results = sim.run_sim(char)
Plot().plot_combined(results)
