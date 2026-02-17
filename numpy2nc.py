'''
Author: Yishuo Wang
Date: 2024-10-19 01:00:23
LastEditors: Yishuo Wang
LastEditTime: 2025-12-20 16:20:14
FilePath: /paper_detection/methods/GBM/numpy2nc.py
Description: the function to convert numpy array to netCDF file and save them

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import netCDF4 as nc
import os 

def convert(sst_data, gradient_data, output_path, name, lon, lat, sst_name, gradient_name):
    # create the netCDF file with dimension of lon and lat
    file_name = os.path.join(output_path, f'{name}.nc')
    f = nc.Dataset(file_name, 'a', format='NETCDF4')
    f.createDimension('lon', len(lon))
    f.createDimension('lat', len(lat))
    # create the variable
    lon_var = f.createVariable('lon', 'f4', ('lon',))
    lat_var = f.createVariable('lat', 'f4', ('lat',))
    sst_var = f.createVariable(sst_name, 'f4', ('lat', 'lon'))
    gradient_var = f.createVariable(gradient_name, 'f4', ('lat', 'lon'))
    # write the data
    lon_var[:] = lon
    lat_var[:] = lat
    sst_var[:] = sst_data
    gradient_var[:] = gradient_data
    f.close()

def convert_feature(front_zone, front_matrix, strength, width, length, output_path, name, lon, lat):
    # create the netCDF file with dimension of lon and lat
    file_name = os.path.join(output_path, f'{name}.nc')
    f = nc.Dataset(file_name, 'a', format='NETCDF4')
    f.createDimension('lon', len(lon))
    f.createDimension('lat', len(lat))
    # create the variable
    lon_var = f.createVariable('lon', 'f4', ('lon',))
    lat_var = f.createVariable('lat', 'f4', ('lat',))
    front_zone_var = f.createVariable('front_zone', 'f4', ('lat', 'lon'))
    front_var = f.createVariable('front_matrix', 'f4', ('lat', 'lon'))
    strength_var = f.createVariable('strength', 'f4', ('lat', 'lon'))
    width_var = f.createVariable('width', 'f4', ('lat', 'lon'))
    length_var = f.createVariable('length', 'f4', ('lat', 'lon'))
    # write the data
    lon_var[:] = lon
    lat_var[:] = lat
    front_zone_var[:] = front_zone
    front_var[:] = front_matrix
    strength_var[:] = strength
    width_var[:] = width
    length_var[:] = length
    f.close()   