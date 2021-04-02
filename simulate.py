# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import math
from datetime import datetime
from datetime import timedelta
from geographiclib.geodesic import Geodesic
import concurrent.futures
import time


class Simulation():
    """
    Attributes
    ----------
    geo : geographiclib.geodesic.Geodesic
        Ellipsoid used to calculaate the new coordinates at each timestep.
    start_time : datetime.datetime
        Start time of the simulated data.
    end_time : datetime.datetime
        End time of the simulated data.
    timestep : float
        Time increment in seconds of the readings.
        
    Methods
    -------
    run():
        Starts the simulation.
    """
    
    def __init__(self,
                 geo = Geodesic.WGS84,
                 start_time = datetime.strptime('01/01/2000 00:00:00',
                                                '%d/%m/%Y %H:%M:%S'),
                 end_time = datetime.strptime('01/01/2000 00:01:00',
                                              '%d/%m/%Y %H:%M:%S'),
                 timestep = 1):
        """"""
        
        self.geo            = geo
        self.start_time     = start_time
        self.end_time       = end_time
        self.timestep       = timestep
        
        
    def runsim(self, char):
        """ """
            
        start_pos = char.start_pos
        velocity_func = char.velocity_func
        lat_func = char.lat_func
        lon_func = char.lon_func
        lat_noise = char.lat_noise
        lon_noise = char.lon_noise
        velocity_func_params = char.velocity_func_params
        lat_func_params = char.lat_func_params
        lon_func_params = char.lon_func_params
        lat_noise_params = char.lat_noise_params
        lon_noise_params = char.lon_noise_params
        
        # duration of sim in seconds
        time_delta = (self.end_time - self.start_time).total_seconds()
        
        # discrete time increments
        increments = np.arange(0, time_delta, self.timestep)
        
        # output columns
        dtime   = [None]*len(increments)
        stime   = [None]*len(increments)
        lat     = [None]*len(increments)
        lon     = [None]*len(increments)
        x_data  = [None]*len(increments)
        y_data  = [None]*len(increments)
        
        lat2 = start_pos[0]
        lon2 = start_pos[1]
        dist2 = 0.
    
        for idx, t in enumerate(increments):
    
            lat1 = lat2
            lon1 = lon2
    
            dist = self.timestep * velocity_func(t, velocity_func_params)
            
            dist1 = dist2 + dist
            dist2 = dist1
    
            y = lat_noise(lat_func(dist1, lat_func_params), lat_noise_params)
            x = lon_noise(lon_func(dist1, lon_func_params), lon_noise_params)
            
            if y == 0 and x >= 0:
                azi = 180.
            elif y == 0 and x < 0:
                azi = 0.
            else:
                azi = math.degrees(math.atan(x/y))
            if y < 0:
                azi = azi+180.
    
            g = self.geo.Direct(lat1, lon1, azi, dist)
    
            lat2 = g['lat2']
            lon2 = g['lon2']
    
            dtime[idx]  = self.start_time + timedelta(seconds=t)
            stime[idx]  = t
            lat[idx]    = lat2
            lon[idx]    = lon2
            x_data[idx] = x
            y_data[idx] = y
        
        return {'dtime': dtime, 'stime': stime, 'lat': lat, 'lon': lon,
                'x': x_data, 'y': y_data}
        
    
    def run_parallel(self, chars=[]):
        """ """
            
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(self.runsim, chars))
            
        

class Character:
    """ """
    
    def __init__(self,
                 start_pos              = (0.,0.),
                 velocity_func          = (lambda t, _ : 1.),
                 lat_func               = (lambda d, _ : d),
                 lon_func               = (lambda d, _ : d),
                 lat_noise              = (lambda o, _ : o),
                 lon_noise              = (lambda o, _ : o),
                 velocity_func_params   = None,
                 lat_func_params        = None,
                 lon_func_params        = None,
                 lat_noise_params       = None,
                 lon_noise_params       = None
                 ):
        """ """
        
        self.start_pos              = start_pos
        self.velocity_func          = velocity_func
        self.lat_func               = lat_func
        self.lon_func               = lon_func
        self.lat_noise              = lat_noise
        self.lon_noise              = lon_noise
        self.velocity_func_params   = velocity_func_params
        self.lat_func_params        = lat_func_params
        self.lon_func_params        = lon_func_params
        self.lat_noise_params       = lat_noise_params
        self.lon_noise_params       = lon_noise_params





char1 = Character()
char2 = Character()

char2.start_pos = (10.,10.)

sim = Simulation()

sim.start_time = datetime.strptime('13/03/21 00:00:00', '%d/%m/%y %H:%M:%S')
sim.end_time = datetime.strptime('13/03/21 00:04:16', '%d/%m/%y %H:%M:%S')

tst = sim.run_parallel([char1, char2])










"""
Parameters
----------
start_time : datetime.datetime
    Start time of the simulated data.
end_time : datetime.datetime
    End time of the simulated data.
timestep : float
    Time increment in seconds of the readings.
travel_speed : float
    Speed in m/s to simulate travel.
start_pos : tuple
    Tuple of latitude and longitude coordinates, indicating the start
    position from which travel begins.
lat_func : function
    Function defining the path to travel from the start_pos latitude
    ordinate until the end_time is reached. Takes total distance travelled
    and lat_func_params as inputs and outputs heading.
lon_func : function
    Function defining the path to travel from the start_pos longitude
    ordinate until the end_time is reached. Takes total distance travelled
    and lon_func_params as inputs and outputs heading.
lat_func_params : dict
    Parameter dictionary for latitude path function.
lon_func_params : dict
    Parameter dictionary for longitude path function.
lat_noise : function
    Noise function that takes lat_func output and lat_noise_params as
    input and outputs modified heading.
lon_noise : function
    Noise function that takes lon_func output and lon_noise_params as
    input and outputs modified heading.
lat_noise_params : dict
    Parameter dictionary for latitude noise function.
lon_noise_params : dict
    Parameter dictionary for longitude noise function.
    
Returns
-------
pandas.DataFrame
    A dataframe of the results of the simulation.
"""
