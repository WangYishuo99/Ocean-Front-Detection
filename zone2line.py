'''
Author: Yishuo Wang
Date: 2024-07-29 16:09:34
LastEditors: Yishuo Wang
LastEditTime: 2025-12-20 15:30:10
FilePath: /paper_detection/methods/GBM/zone2line.py
Description: the function making front zone to front line 

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
from skimage import morphology
import numpy as np

import edge_following
import edge_merging
import ring_deletion
import edge_pruning_MSF
import front_matrix_construction

merge_radius = 3

# set the flag to control if the ring deletion is needed
flag = True

def zone2line(marked_matrix, gradient_direction, type_now):
    converted_matrix = marked_matrix.copy()
    # make the nan values be 0
    converted_matrix[np.where(np.isnan(converted_matrix))] = 0

    # 1.calculate the skeleton and distance
    skel, distance =morphology.medial_axis(converted_matrix, return_distance=True)

    # 3. prune the skeleton by MSF
    skel_MSF, pruned_G_MSF = edge_pruning_MSF.prune_spider_web_by_msf(skel, distance)

    # 4. follow the edges to get the fronts
    fronts = edge_following.follow(skel_MSF, gradient_direction)

    # 5. merge the fronts
    edge_merging.merge(fronts, merge_radius, gradient_direction)

    # 6. discard the ring strcutures iteratively
    while flag:
        fronts_new = ring_deletion.delete_ring(fronts[:])
        if fronts_new == fronts:
            break
        else:
            fronts = fronts_new
    
    # 7. discard the fronts shorter than >=100km
    if type_now == 'SST':
        fronts_new = [front for front in fronts if len(front) >= 20]
    elif type_now == 'SSS':
        fronts_new = [front for front in fronts if len(front) >= 11]

    # 8. generate the front matrix
    front_matrix = front_matrix_construction.construction(fronts_new, marked_matrix)

    return front_matrix, distance, fronts_new