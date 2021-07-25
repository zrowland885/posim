# -*- coding: utf-8 -*-
"""
Created on Sat Apr  3 22:26:25 2021

@author: zrowl
"""

import types
from geographiclib.geodesic import Geodesic

from paths import linear

def coords2path(coords=[], geo=Geodesic.WGS84, interp_func_name='linear'):
    
    lat_funcstr = "def lat_path(d, _):"
    lon_funcstr = "def lon_path(d, _):"
    
    d = 0.
    
    for i in range(len(coords)-1):
        
        g = geo.Inverse(coords[i][0], coords[i][1],
                        coords[i+1][0], coords[i+1][1])
        azi = g['azi1']
        d = d + g['s12']
        
        if i==0:
            ifstate = "if"
        elif i>0:
            ifstate = "elif"
        
        lat_line = ifstate + " d < "+str(d)+": \
            return " + interp_func_name + "(d, {'ordinate': 'lat', 'aziDeg': "+str(azi)+"})"
        lon_line = ifstate + " d < "+str(d)+": \
            return " + interp_func_name + "(d, {'ordinate': 'lon', 'aziDeg': "+str(azi)+"})"
        
        lat_funcstr = lat_funcstr + "\n\t" + lat_line
        lon_funcstr = lon_funcstr + "\n\t" + lon_line
    
    lat_funcstr = lat_funcstr + "\n\t" + "else: return 0"
    lon_funcstr = lon_funcstr + "\n\t" + "else: return 0"
    
    lat_funcobj = compile(lat_funcstr, '<string>', 'exec')
    lon_funcobj = compile(lon_funcstr, '<string>', 'exec')
    
    lat_functype = types.FunctionType(lat_funcobj.co_consts[0], globals())
    lon_functype = types.FunctionType(lon_funcobj.co_consts[0], globals())
    
    return lat_functype, lon_functype, lat_funcstr, lon_funcstr, d
