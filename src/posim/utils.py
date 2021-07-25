# -*- coding: utf-8 -*-
"""
Created on Tue Mar 16 21:39:24 2021

@author: zrowl
"""

def convert_images(filetype, read_dir, write_dir=None):
    import os
    from PIL import Image
    
    if write_dir == None:
        write_dir = read_dir
    
    _, _, files = next(os.walk(read_dir))
    
    for f in files:
        img = Image.open(read_dir+f).convert('L')
        filename = os.path.splitext(f)[0]
        path = write_dir+filename+filetype
        img.save(path)

read_dir = 'output_old3/'
write_dir = 'output/'
filetype = '.png'

convert_images(filetype, read_dir, write_dir)
