'''
Author: Yishuo Wang
Date: 2024-10-21 11:55:33
LastEditors: Yishuo Wang
LastEditTime: 2025-12-20 17:13:07
FilePath: /paper_detection/methods/GBM/execution.py
Description: the outer function for the whole process

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import gradient_front_zone
import pickle
import numpy2nc as n2nc
import zone2line as z2l
import length_width_strength_calculation as lwsc

import os
import netCDF4 as nc
import gc

def whole_function(date, analysisType, input, output, beginLon, endLon, beginLat, endLat, type_now, region_name):
    date = str(date)
    year = date[0:4]

    # 判断是否已经有文件了，如果有就不再处理
    path_temp = os.path.join(output, region_name, analysisType, type_now, 'feature', 'nc', date + '.nc')
    if os.path.exists(path_temp):
        return
    
    input_path = os.path.join(input, type_now, year)
    
    file_path = os.path.join(input_path, f'{date}.nc')

    if not os.path.exists(file_path):
        return
    else:
        print(f'Processing {file_path}...')

    # 0.读文件
    with nc.Dataset(file_path) as data:
        # 1.计算梯度和锋区
        sst, gradient_magnitude, gradient_direction, marked_matrix, lon_extracted, lat_extracted = gradient_front_zone.get_gradient_front_zone(data, beginLon, endLon, beginLat, endLat, type_now)

    # 2.将梯度与温度写入nc文件
    output_nc_path = os.path.join(output, region_name, analysisType, type_now, 'gradient', 'nc')
    os.makedirs(output_nc_path, exist_ok = True)
    n2nc.convert(sst, gradient_magnitude, output_nc_path, date, lon_extracted, lat_extracted, type_now, 'gradient_magnitude')

    # 3.计算锋面和距离
    front_matrix, distance, fronts = z2l.zone2line(marked_matrix, gradient_direction, type_now)

    # 4.计算强度、宽度、长度
    strength = lwsc.strength_calculation(gradient_magnitude, fronts)
    width = lwsc.width_calculation(gradient_magnitude.shape, distance, fronts, type_now)
    length = lwsc.length_calculation(gradient_magnitude.shape, fronts, type_now)

    # 5.将锋区、锋面、强度、宽度、长度写入nc文件
    output_nc_path = os.path.join(output, region_name, analysisType, type_now, 'feature', 'nc')
    os.makedirs(output_nc_path, exist_ok = True)
    n2nc.convert_feature(marked_matrix, front_matrix, strength, width, length, output_nc_path, date, lon_extracted, lat_extracted)

    # 6.将锋面写入矢量文件
    output_pkl_path = os.path.join(output, region_name, analysisType, type_now, 'vector', 'pkl')
    os.makedirs(output_pkl_path, exist_ok = True)
    output_pkl_name = os.path.join(output_pkl_path, f'{date}.pkl')
    with open(output_pkl_name, 'wb') as f:
        pickle.dump(fronts, f)
        
    # 主动释放大数组内存
    gc.collect()