# -*- coding: utf-8 -*-

import numpy as np
import math
import concurrent.futures
from datetime import datetime
from datetime import timedelta
from geographiclib.geodesic import Geodesic


class Simulation:
    """
    Attributes
    ----------
    geo : geographiclib.geodesic.Geodesic
        Ellipsoid used to calculaate the new coordinates at each timestep.
    start_time : datetime.datetime / float / int
        Start time of the simulated data.
    end_time : datetime.datetime / float / int
        End time of the simulated data.
    timestep : float
        Time increment in seconds of the readings.
        
    Methods
    -------
    
    __init__():
        Constructs all the attributes for the Simulation object.
    
    run_sim(char):
        Runs a simulation instance.
    
    run_threaded(chars):
        Runs simulation instances in seperate threads for multiple Characters.
    """
    
    def __init__(self):
        """
        Constructs all the attributes for the Simulation object.
        
        Parameters
        ----------
        geo : geographiclib.geodesic.Geodesic
            Ellipsoid used to calculaate the new coordinates at each timestep.
        start_time : datetime.datetime / float / int
            Start time of the simulated data.
        end_time : datetime.datetime / float / int
            End time of the simulated data.
        timestep : float
            Time increment in seconds of the readings.
        """
        
        self.geo = Geodesic.WGS84
        self.start_time = datetime.strptime('01/01/2000 00:00:00',
                                                '%d/%m/%Y %H:%M:%S')
        self.end_time = datetime.strptime('01/01/2000 00:01:00',
                                              '%d/%m/%Y %H:%M:%S')
        self.timestep = 1

    def run_sim(self, char):
        """
        Runs a simulation instance.
        
        Parameters
        ----------
        char : Character
            Instance of the Character class.
        
        Returns
        -------
        dict
            Dictionary of the simulation data:
            - name: Name of the character
            - dtime: Datetime / numeric time at each time increment
            - stime: Total time elapsed since the start of the simulation
            - lat: Latitude at each increment based on the geo ellipsoid
            - lon: Longitude at each increment based on the geo ellipsoid
            - y: Y component of the direction vector
            - x: X component of the direction vector
        """
        
        # Type check start_time and end_time
        if all(isinstance(input_time, datetime) for input_time in
               [self.start_time, self.end_time]):
            self.time_type = 'datetime'
        elif all(isinstance(input_time, (int, float)) for input_time in
               [self.start_time, self.end_time]):
            self.time_type = 'numeric'
        
        # Get attributes of the simulated character
        name = char.name
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
        
        # Duration of sim in seconds (or whichever units are represented in
        # numeric time)
        if self.time_type == 'datetime':
            time_delta = (self.end_time - self.start_time).total_seconds()
        elif self.time_type == 'numeric':
            time_delta = self.end_time - self.start_time
        else:
            raise TypeError("start_time and end_time must both be either \
                            datetime.datetime, int or float type.")
        
        # Discrete time increments
        increments = np.arange(0, time_delta, self.timestep)
        
        # Output lists
        dtime   = [None]*len(increments)
        stime   = [None]*len(increments)
        lat     = [None]*len(increments)
        lon     = [None]*len(increments)
        y_data  = [None]*len(increments)
        x_data  = [None]*len(increments)
        
        # Initialise the latitude, longitude and total distance travelled
        lat2 = start_pos[0]
        lon2 = start_pos[1]
        dist2 = 0.
        
        # Iterate over the time increments of the sim
        for idx, t in enumerate(increments):
    
            # Set to lat/lon of previous increment
            lat1 = lat2
            lon1 = lon2
            
            # Calculate the distance to travel for this increment
            dist = self.timestep * velocity_func(t, velocity_func_params)
            
            # Increment the total distance travelled
            dist1 = dist2 + dist
            dist2 = dist1
                
            # Calculate the opposite and adjacent components of the direction
            # vector
            y = lat_noise(lat_func(dist1, lat_func_params), lat_noise_params)
            x = lon_noise(lon_func(dist1, lon_func_params), lon_noise_params)
            
            # Calculate the azimuth angle of the direction vector
            if y == 0 and x >= 0:
                azi = 180.
            elif y == 0 and x < 0:
                azi = 0.
            else:
                azi = math.degrees(math.atan(x/y))
            if y < 0:
                azi = azi+180.
                
            # Calculate the new latitude and longitude
            g = self.geo.Direct(lat1, lon1, azi, dist)
    
            lat2 = g['lat2']
            lon2 = g['lon2']
            
            # Calculate the time elapsed since the start_time of the sim (in
            # seconds or otherwise)
            if self.time_type == 'datetime':
                dtime[idx]  = self.start_time + timedelta(seconds=t)
            elif self.time_type == 'numeric':
                dtime[idx]  = self.start_time + t
            
            # Fill the output lists
            stime[idx]  = t
            lat[idx]    = lat2
            lon[idx]    = lon2
            y_data[idx] = y
            x_data[idx] = x
        
        return {'name': name, 'dtime': dtime, 'stime': stime, 'lat': lat,
                'lon': lon, 'y': y_data, 'x': x_data}
        
    def run_threaded(self, chars=[]):
        """
        Runs simulation instances in seperate threads for multiple Characters.
        
        Parameters
        ----------
        chars : list
            List of Character instances.
        
        Returns
        -------
        list
            List of dictionaries containing the results of each simulation.
        """
            
        with concurrent.futures.ThreadPoolExecutor() as executor:
            return list(executor.map(self.run_sim, chars))
            

class Character:
    """
    Attributes
    ----------
    name : str
        Name of the character (for plotting legends etc.)
    start_pos : tuple
        Tuple of latitude and longitude coordinates, indicating the start
        position from which travel begins.
    velocity_func : function
        Function defining the travel velocity in metres per second (or
        whichever time unit is used).
    lat_func : function
        Function defining the path to travel from the start_pos latitude
        ordinate until the end_time is reached. Takes total distance travelled
        and lat_func_params as inputs and outputs heading.
    lon_func : function
        Function defining the path to travel from the start_pos longitude
        ordinate until the end_time is reached. Takes total distance travelled
        and lon_func_params as inputs and outputs heading.
    lat_noise : function
        Noise function that takes lat_func output and lat_noise_params as
        input and outputs modified heading.
    lon_noise : function
        Noise function that takes lon_func output and lon_noise_params as
        input and outputs modified heading.
    velocity_func_params : dict
        Parameter dictionary for velocity function.
    lat_func_params : dict
        Parameter dictionary for latitude path function.
    lon_func_params : dict
        Parameter dictionary for longitude path function.
    lat_noise_params : dict
        Parameter dictionary for latitude noise function.
    lon_noise_params : dict
        Parameter dictionary for longitude noise function.
    
    Methods
    -------
    
    __init__():
        Constructs all the attributes for the Simulation object.
    
    """
    
    def __init__(self):
        """
        Constructs all the attributes for the Simulation object.
        
        Parameters
        ----------
        name : str
            Name of the character (for plotting legends etc.)
        start_pos : tuple
            Tuple of latitude and longitude coordinates, indicating the start
            position from which travel begins.
        velocity_func : function
            Function defining the travel velocity in metres per second (or
            whichever time unit is used).
        lat_func : function
            Function defining the path to travel from the start_pos latitude
            ordinate until the end_time is reached. Takes total distance travelled
            and lat_func_params as inputs and outputs heading.
        lon_func : function
            Function defining the path to travel from the start_pos longitude
            ordinate until the end_time is reached. Takes total distance travelled
            and lon_func_params as inputs and outputs heading.
        lat_noise : function
            Noise function that takes lat_func output and lat_noise_params as
            input and outputs modified heading.
        lon_noise : function
            Noise function that takes lon_func output and lon_noise_params as
            input and outputs modified heading.
        velocity_func_params : dict
            Parameter dictionary for velocity function.
        lat_func_params : dict
            Parameter dictionary for latitude path function.
        lon_func_params : dict
            Parameter dictionary for longitude path function.
        lat_noise_params : dict
            Parameter dictionary for latitude noise function.
        lon_noise_params : dict
            Parameter dictionary for longitude noise function.
        """
        
        self.name                   = 'Character'
        self.start_pos              = (0.,0.)
        self.velocity_func          = (lambda t, _ : 1.)
        self.lat_func               = (lambda d, _ : d)
        self.lon_func               = (lambda d, _ : d)
        self.lat_noise              = (lambda o, _ : o)
        self.lon_noise              = (lambda o, _ : o)
        self.velocity_func_params   = None
        self.lat_func_params        = None
        self.lon_func_params        = None
        self.lat_noise_params       = None
        self.lon_noise_params       = None


class Plot:
    """
    Attributes
    ----------
    ...
        
    Methods
    -------
    
    __init__():
        ...
    
    plot_coordinates_combined(results):
        Plots latitude against longitude, latitude against time and longitude
        against time as seperate axes in the same figure.
        
    plot_coordinates(results):
        Plots latitude against longitude.
    """
    
    def __init__(self):
        pass
        
    def plot_combined(self, results, legend=True):
        """
        Plots latitude against longitude, latitude against time and longitude
        against time as seperate axes in the same figure.
        
        Parameters
        ----------
        results : list / dict
            Dictionary or list of dictionaries of results returned by
            Simulation.run_sim or Simulation.run_threaded methods.
        """
        import matplotlib.pyplot as plt
        from matplotlib.gridspec import GridSpec
        
        fig = plt.figure(figsize=(10, 10))
        gs = GridSpec(nrows=2, ncols=2, wspace=0.3, hspace=0.3,
                      height_ratios=[2,1])
        
        ax0 = fig.add_subplot(gs[1, 0])
        ax1 = fig.add_subplot(gs[1, 1])
        ax2 = fig.add_subplot(gs[0, :])
        
        if not isinstance(results, list):
            results = [results]
        
        for result in results:    
            ax0.scatter(x=result['stime'], y=result['lat'], s=.8)    
            ax1.scatter(x=result['stime'], y=result['lon'], s=.8)
            ax2.scatter(x=result['lon'], y=result['lat'], s=.8,
                        label=result['name'])
        
        ax0.set_xlabel('stime')
        ax0.set_ylabel('lat')

        ax1.set_xlabel('stime')
        ax1.set_ylabel('lon')
        
        ax2.set_xlabel('lon')
        ax2.set_ylabel('lat')
        plt.xticks(rotation=90)
        
        fig.suptitle("plot_coordinates_combined")
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)
        
        if legend:
            plt.legend()
            
        plt.show()
        
    def plot_single(self, results, xlabel, ylabel, fig_title):
        """
        Plots xlabel values against ylabel values.
        
        Parameters
        ----------
        results : list / dict
            Dictionary or list of dictionaries of results returned by
            Simulation.run_sim or Simulation.run_threaded methods.
        xlabel : str
            Key to retrieve the x axis values from results.
        ylabel : str
            Key to retrieve the y axis values from results.
        fig_title : str
            Title of the figure.
        """
        import matplotlib.pyplot as plt
        
        fig = plt.figure(figsize=(10, 10))
        
        ax = fig.add_subplot()
        
        if not isinstance(results, list):
            results = [results]
        
        for result in results:
            ax.scatter(x=result[xlabel], y=result[ylabel], s=.8,
                        label=result['name'])

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.xticks(rotation=90)
        
        fig.suptitle(fig_title)
        fig.tight_layout()
        fig.subplots_adjust(top=0.95)
        
        plt.legend()
        plt.show()

    def plot_coordinates(self, results):
        """ Plots latitude against longitude. """
        
        xlabel = 'lon'
        ylabel = 'lat'
        fig_title = "plot_coordinates"
        
        self.plot_single(results, xlabel, ylabel, fig_title)
        
    def plot_xy(self, results):
        """ Plots x vectors against y vectors. """
        
        xlabel = 'x'
        ylabel = 'y'
        fig_title = "plot_xy"
        
        self.plot_single(results, xlabel, ylabel, fig_title)
        
    def plot_lat_over_time(self, results):
        """ Not implemented """
        raise NotImplementedError
    
    def plot_lon_over_time(self, results):
        """ Not implemented """
        raise NotImplementedError
