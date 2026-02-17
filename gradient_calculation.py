'''
Author: Yishuo Wang
Date: 2024-03-13 13:35:43
LastEditors: Yishuo Wang
LastEditTime: 2025-12-05 11:04:05
FilePath: /paper_detection/methods/GBM/gradient_calculation.py
Description: calculate the gradient magnitude and direction, plot and save them

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''

from scipy.ndimage import sobel
import numpy as np

def magnitude_and_direction_gradient(SST, type_now):
    if type_now == 'SST':
        resolution = 5
    elif type_now == 'SSS':
        resolution = 9

    gradient_x = sobel(SST, axis=0)
    gradient_y = sobel(SST, axis=1)

    # Calculate the gradient magnitude
    gradient_magnitude = np.hypot(gradient_x, gradient_y)

    # change the unit
    gradient_magnitude = gradient_magnitude / resolution

    # Calculate the gradient direction
    # the range is -pi to pi
    gradient_direction = np.arctan2(gradient_y, gradient_x)

    return gradient_magnitude, gradient_direction

