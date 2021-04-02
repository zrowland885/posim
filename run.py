# -*- coding: utf-8 -*-
"""
time, lat, lon, alt
2021/03/09 19:51:36.000688,42.188068390,-8.711703300,159.781936646
"""

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm
import matplotlib.tri as tri

from datetime import datetime
import random
import numpy as np
import pandas as pd

from simulate import simulate_position
import paths, noise, velocities


def norm(x):
    return (x-min(x))/(max(x)-min(x))
    

# INPUTS
start_time = datetime.strptime('13/03/21 00:00:00', '%d/%m/%y %H:%M:%S')
end_time = datetime.strptime('13/03/21 00:04:16', '%d/%m/%y %H:%M:%S')
timestep = 1
start_pos = (0.,0.)

plot_type = 1

# PARAMETERS
circle_params = {'radius': 0.}
ellipse_params = {'maj_ax': 0., 'min_ax': 0.}
ellipse_rotate_params = {'x0': 0., 'y0': 0., 'aziDeg': 0., 'maj_ax': 0., 'min_ax': 0.}
noise_rand_params = {'min': 0., 'max': 0.}
velocity_rand_params = {'min': 0., 'max': 0.}
linear_params = {'aziDeg': 0.}

# ITERATION
samples = 100
filepaths = [None]*samples
ftypes = [None]*samples

for fid in range(0,samples):
    
    # RANDOMISE PARAMETERS WITHIN BOUNDS
    ellipse_rotate_params['aziDeg'] = random.uniform(0, 359)
    ellipse_rotate_params['maj_ax'] = random.uniform(15, 30)
    ellipse_rotate_params['min_ax'] = random.uniform(5, 15)
    noise_rand_params['min'] = random.uniform(-0.5, 0.5)
    noise_rand_params['max'] = random.uniform(1.5, 2.5)
    velocity_rand_params['min'] = random.uniform(-0.5, 0.5)
    velocity_rand_params['max'] = random.uniform(1.5, 2.)
    linear_params['aziDeg'] = random.uniform(0, 359)
    
    
    # ASSIGN FUNCTIONS AND PARAMS
    if fid >= 40:
        ftypes[fid] = 1 # mark as non-ellipse type
        
        func_option = random.randrange(4)
        if func_option == 0:
            #fname = 'output/sim_'+str(fid)+'_linear.csv'
            fname = 'data/sim_'+str(fid)+'_linear.jpg'
            lat_func = paths.linear_lat
            lon_func = paths.linear_lon
            path_params = linear_params
            print(fname)
        if func_option == 1:
            #fname = 'output/sim_'+str(fid)+'_sine.csv'
            fname = 'data/sim_'+str(fid)+'_sine.jpg'
            lat_func = paths.sine
            lon_func = paths.sine
            path_params = None
            print(fname)
        if func_option == 2:
            #fname = 'output/sim_'+str(fid)+'_cosine.csv'
            fname = 'data/sim_'+str(fid)+'_cosine.jpg'
            lat_func = paths.cosine
            lon_func = paths.cosine
            path_params = None
            print(fname)
        if func_option == 3:
            #fname = 'output/sim_'+str(fid)+'_tan.csv'
            fname = 'data/sim_'+str(fid)+'_tan.jpg'
            lat_func = paths.tan
            lon_func = paths.tan
            path_params = None
            print(fname)            
    
    else:
        ftypes[fid] = 0 # mark as ellipse type
        
        fname = 'data/sim_'+str(fid)+'_ellipse.jpg'
        lat_func = paths.ellipse_rotate_maj
        lon_func = paths.ellipse_rotate_min
        path_params = ellipse_rotate_params
        print(fname)
    
    noise_func = noise.random
    noise_params = noise_rand_params
    
    velocity_func = velocities.random
    velocity_func_params = velocity_rand_params
    
    lat_func_params = path_params
    lon_func_params = path_params
    lat_noise = noise_func
    lon_noise = noise_func
    lat_noise_params = noise_params
    lon_noise_params = noise_params
    
    # GET RESULTS
    df_results = simulate_position(start_time,
                                   end_time,
                                   timestep,
                                   start_pos,
                                   velocity_func,
                                   velocity_func_params,
                                   lat_func=lat_func,
                                   lon_func=lon_func,
                                   lat_func_params=lat_func_params,
                                   lon_func_params=lon_func_params,
                                   lat_noise=lat_noise,
                                   lon_noise=lon_noise,
                                   lat_noise_params=lat_noise_params,
                                   lon_noise_params=lon_noise_params)
    
    # EXPORT
    export_times = df_results['time'].to_list()
    
    x = np.cos(df_results['lat'])*np.cos(df_results['lon'])
    y = np.cos(df_results['lat'])*np.sin(df_results['lon'])
    z = np.sin(df_results['lat'])
    
    x_norm = norm(x)
    y_norm = norm(y)
    z_norm = norm(z)
    
    df_export = pd.DataFrame({'t': export_times,
                              'x': x_norm, 'y': y_norm, 'z': z_norm})
    
    #df_export.to_csv(fname, index=False, header=False)
    
    filepaths[fid] = './'+fname
    
    # PLOT
    
    if plot_type == 0:
        # Set equal axis scales so shape of path is clear in lat/lon plot
        lat_max = df_results['lat'].max()
        lat_min = df_results['lat'].min()
        lon_max = df_results['lon'].max()
        lon_min = df_results['lon'].min()
        lim_max = max(lat_max, lon_max)
        lim_min = min(lat_min, lon_min)
        lim = (lim_min*1.1, lim_max*1.1)
        
        fig = plt.figure(figsize=(10, 10))
        gs = GridSpec(nrows=2, ncols=2, wspace=0.4, hspace=0.4)
        ax0 = fig.add_subplot(gs[1, 0])
        df_results.plot.scatter(x="time", y="lat", s=.8, ax=ax0)
        ax1 = fig.add_subplot(gs[1, 1])
        df_results.plot.scatter(x="time", y="lon", s=.8, ax=ax1)
        
        ax2 = fig.add_subplot(gs[0, 0])#(gs[0, :])
        ax2.set_aspect('equal')
        df_results.plot.scatter(x="lon", y="lat", s=.8, xlim=lim, ylim=lim, ax=ax2)
        plt.xticks(rotation=90)
        
        fig.suptitle(fname)
        
        ax3 = fig.add_subplot(gs[0, 1])
        ax3.set_xlabel('normalised x')
        ax3.set_ylabel('normalised y')
        ax3.scatter(x=x_norm, y=y_norm, c=z_norm, s=5)
        #ax3.tricontourf(x_norm, y_norm, z_norm, 20)
    
        plt.show()
    
    elif plot_type == 1:
        # EXPORT IMG
    
        dpi = 96
        plt.figure(figsize=(28/dpi, 28/dpi), dpi=dpi)
        plt.scatter(x=x_norm, y=y_norm, c=z_norm, s=0.05)#, colorbar=False)
        plt.axis('off')
        
        plt.savefig(fname)
        
    

df_files = pd.DataFrame({'x': filepaths, 'y': ftypes})

df_files.to_csv('filepaths.csv', index=False)
