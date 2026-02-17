'''
Author: Yishuo Wang
Date: 2024-06-27 16:05:39
LastEditors: Yishuo Wang
LastEditTime: 2025-12-20 16:10:46
Description: the function is to calculate the length, width and strength of the detected fronts
'''
import numpy as np

def _flatten_data(data):
    """把 data(list[list[(x,y)]]) 转成 1D x,y,gid 三个 NumPy 数组。"""
    xs = []
    ys = []
    gids = []

    for gid, pts in enumerate(data):
        # 你提供的是 tuple，所以 array 转换开销很小
        arr = np.array(pts, dtype=np.int32)
        xs.append(arr[:, 0])
        ys.append(arr[:, 1])
        gids.append(np.full(len(arr), gid, dtype=np.int32))

    return (np.concatenate(xs),
            np.concatenate(ys),
            np.concatenate(gids))


def strength_calculation(magnitude, data):
    strength = np.full_like(magnitude, np.nan)

    all_x, all_y, group_id = _flatten_data(data)
    vals = magnitude[all_x, all_y]

    group_sum = np.bincount(group_id, weights=vals)
    group_cnt = np.bincount(group_id)
    group_avg = group_sum / group_cnt

    strength[all_x, all_y] = group_avg[group_id]
    return strength


def width_calculation(shape, distance, data, type_now):
    if type_now == 'SST':
        resolution = 5
    elif type_now == 'SSS':
        resolution = 9

    width = np.full(shape, np.nan)

    all_x, all_y, group_id = _flatten_data(data)
    vals = distance[all_x, all_y]

    group_sum = np.bincount(group_id, weights=vals)
    group_cnt = np.bincount(group_id)
    group_avg = group_sum / group_cnt    # 平均距离

    width[all_x, all_y] = group_avg[group_id] * resolution * 2
    return width


def length_calculation(shape, data, type_now):
    if type_now == 'SST':
        resolution = 5
    elif type_now == 'SSS':
        resolution = 9
        
    length = np.full(shape, np.nan)

    all_x, all_y, group_id = _flatten_data(data)

    # 每个点贡献 1
    cnt = np.bincount(group_id, weights=np.ones_like(group_id))
    length_group = cnt * resolution

    length[all_x, all_y] = length_group[group_id]
    return length
