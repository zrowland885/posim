# -*- coding: utf-8 -*-
"""
An example of converting a list of coordinates to a linear path function, then
simulating the path with some noise.
"""

from posim import simulate, noise, convert
from datetime import datetime
import time


# Velocity function to stop the character once they reach a certain stop time
# (numeric, or in this case in terms of seconds elapsed)
def velocity_func(t, params):
    if t < params['stop_time']:
        return params['velocity']
    else:
        return 0

# Define the walk speed (in metres per numeric time, here seconds)
walk_speed = 1.

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
latf, lonf, latfstr, lonfstr, dist = convert.coords2path(snowdon_pyg_wgs84)

# Time elapsed in seconds
stop_time = dist / walk_speed

# To find the time elapsed during the walk in hh:mm:ss
stop_time_hhmmss = time.strftime('%H:%M:%S', time.gmtime(stop_time))

# Create a character instance with some noise
char = simulate.Character()
char.lat_func = latf
char.lon_func = lonf
char.lat_noise = noise.random
char.lon_noise = noise.random
noise_params = {'min': 0., 'max': 2.}
char.lat_noise_params = noise_params
char.lon_noise_params = noise_params
char.velocity_func = velocity_func
char.velocity_func_params = {'velocity': walk_speed, 'stop_time': stop_time}

# Create the simulation
# The route takes about 1:22 hrs at 1 m/s. According to google maps it should
# take 1:24 hrs so this makes sense given an uphill pace.
sim = simulate.Simulation()
sim.start_time = datetime.strptime('01/01/21 00:00:00', '%d/%m/%y %H:%M:%S')
sim.end_time = datetime.strptime('01/01/21 01:20:00', '%d/%m/%y %H:%M:%S')
sim.timestep = 30

# Plot the results
results = sim.run_sim(char)
simulate.Plot().plot_combined(results)
