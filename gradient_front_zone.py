'''
Author: Yishuo Wang
Date: 2024-07-29 14:24:58
LastEditors: Yishuo Wang
LastEditTime: 2025-12-05 11:03:24
FilePath: /paper_detection/methods/GBM/gradient_front_zone.py
Description: calculate the gradient and front zone of the 4 regions

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np
import gradient_calculation
import threshold
import bayesian_plus

# Define the thresholds
upper_threshold = 90
lower_threshold = 60

def get_gradient_front_zone(data, beginLon, endLon, beginLat, endLat, type_now):
    # 1. prepossess and filter the data
    lon = data.variables['lon'][:]
    lat = data.variables['lat'][:]
    
    beginLon = float(beginLon)
    endLon = float(endLon)
    beginLat = float(beginLat)
    endLat = float(endLat)
    
    # condiser the situation that the beginLon is larger than the endLon
    if beginLon > endLon:
        lon_index_east = np.where((lon >= beginLon) & (lon < 180))[0]
        lon_index_west = np.where((lon >= -180) & (lon < endLon))[0]
        lat_index = np.where((lat >= beginLat) & (lat < endLat))[0]

        lon_extracted = np.concatenate((lon[lon_index_east], lon[lon_index_west]), axis = 0)
        lat_extracted = lat[lat_index]

        if type_now == 'SST':
            # if it is sst, then should minus 273.15 and treat the nan values
            data_temp_east = data.variables['analysed_sst'][:, lat_index, lon_index_east]
            data_temp_west = data.variables['analysed_sst'][:, lat_index, lon_index_west]
            data_temp_east = data_temp_east[0]
            data_temp_west = data_temp_west[0]
            # data_temp_east = data_temp_east - 273.15
            # data_temp_west = data_temp_west - 273.15
            data_temp_east = np.array(data_temp_east)
            data_temp_west = np.array(data_temp_west)
            data_temp_east[np.where(data_temp_east > 100)] = np.nan
            data_temp_east[np.where(data_temp_east < -100)] = np.nan
            data_temp_west[np.where(data_temp_west > 100)] = np.nan
            data_temp_west[np.where(data_temp_west < -100)] = np.nan
            data_temp = np.concatenate((data_temp_east, data_temp_west), axis = 1)
        elif type_now == 'SSS':
            data_temp_east = data.variables['sss'][lat_index, lon_index_east]
            data_temp_west = data.variables['sss'][lat_index, lon_index_west]
            data_temp_east = np.array(data_temp_east)
            data_temp_west = np.array(data_temp_west)
            data_temp_east[np.where(data_temp_east > 100)] = np.nan
            data_temp_east[np.where(data_temp_east < -100)] = np.nan
            data_temp_west[np.where(data_temp_west > 100)] = np.nan
            data_temp_west[np.where(data_temp_west < -100)] = np.nan
            data_temp = np.concatenate((data_temp_east, data_temp_west), axis = 1)

    # normal situation
    else:
        lon_index = np.where((lon >= beginLon) & (lon < endLon))[0]
        lat_index = np.where((lat >= beginLat) & (lat < endLat))[0]

        lon_extracted = lon[lon_index]
        lat_extracted = lat[lat_index]

        if type_now == 'SST':
            # if it is sst, then should minus 273.15 and treat the nan values
            data_temp = data.variables['analysed_sst'][:, lat_index, lon_index]
            data_temp = data_temp[0]
            # data_temp = data_temp - 273.15
            data_temp = np.array(data_temp)
            data_temp[np.where(data_temp > 100)] = np.nan
            data_temp[np.where(data_temp < -100)] = np.nan
        elif type_now == 'SSS':
            data_temp = data.variables['sss'][lat_index, lon_index]
            data_temp = np.array(data_temp)
            data_temp[np.where(data_temp > 100)] = np.nan
            data_temp[np.where(data_temp < -100)] = np.nan

    # 2. gradient
    gradient_magnitude, gradient_direction = gradient_calculation.magnitude_and_direction_gradient(data_temp, type_now)
    
    # 3. front_zone
    marked_matrix, p10, p20 = threshold.thresholds_calculation(gradient_magnitude, upper_threshold, lower_threshold)

    marked_matrix = bayesian_plus.bayesian_vectorized(marked_matrix, p10, p20, gradient_magnitude, data_temp)

    marked_matrix[np.where(marked_matrix == 2)] = 0
    
    return data_temp, gradient_magnitude, gradient_direction, marked_matrix, lon_extracted, lat_extracted