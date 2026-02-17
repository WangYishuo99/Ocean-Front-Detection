'''
Author: Yishuo Wang
Date: 2025-11-18 15:49:08
LastEditors: Yishuo Wang
LastEditTime: 2025-11-27 13:33:06
FilePath: /paper_detection/methods/GBM/bayesian_plus.py
Description: accelerated bayesian method with vectorized LDE and BD calculation

Copyright (c) 2025 by Yishuo Wang, All Rights Reserved. 
'''
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from numba import njit, prange

epsilon = 1e-6
LDE_threshold = 0.1
BD_threshold  = 0.1

# ------------------------
# LDE & BD 计算 (完全向量化)
# ------------------------
def compute_LDE_BD(SST):
    rows, cols = SST.shape
    SST_pad = np.pad(SST, 1, constant_values=np.nan)
    windows = sliding_window_view(SST_pad, (3,3))
    windows_flat = windows.reshape(rows, cols, 9)
    neighbor_vector = np.delete(windows_flat, 4, axis=2)  # 去掉中心点

    all_nan_mask = np.all(np.isnan(neighbor_vector), axis=2)

    v_max  = np.nanmax(neighbor_vector, axis=2)
    v_min  = np.nanmin(neighbor_vector, axis=2)
    v_mean = np.nanmean(neighbor_vector, axis=2)

    pair_idx = [(0,7),(1,6),(2,5),(3,4)]
    sum_lde = np.zeros((rows, cols), dtype=np.float64)
    sum_bd  = np.zeros((rows, cols), dtype=np.float64)
    count_pairs = np.zeros((rows, cols), dtype=np.float64)

    for a,b in pair_idx:
        valid_mask = (~np.isnan(neighbor_vector[:,:,a])) & (~np.isnan(neighbor_vector[:,:,b]))
        count_pairs += valid_mask
        sum_lde += np.where(valid_mask,
                             4/7*(v_max - v_mean - np.abs(neighbor_vector[:,:,a]-neighbor_vector[:,:,b]))/(v_max - v_min + epsilon)+0.5,
                             0.0)
        sum_bd += np.where(valid_mask,
                           np.abs(neighbor_vector[:,:,a]-neighbor_vector[:,:,b])/(v_max - v_min + epsilon),
                           0.0)

    count_safe = np.where(count_pairs==0, np.nan, count_pairs)
    LDE = sum_lde / count_safe
    BD  = sum_bd  / count_safe
    LDE[all_nan_mask] = np.nan
    BD[all_nan_mask] = np.nan
    return LDE, BD

# ------------------------
# 批量贝叶斯决策 (Numba)
# ------------------------
@njit(parallel=True)
def compute_posterior_batch(idx_flat, marked_matrix_out, prior_flat, LDE_flat, BD_flat, grad_flat, rows, cols):
    for idx_ptr in prange(len(idx_flat)):
        idx = idx_flat[idx_ptr]
        ii = idx // cols
        jj = idx % cols

        grad_p = grad_flat[idx]
        LDE_p = LDE_flat[idx]
        BD_p  = BD_flat[idx]
        prior_p = prior_flat[idx]

        # Masks for all points
        front_mask = grad_flat > grad_p
        nonfront_mask = grad_flat < grad_p

        # LDE / BD similarity masks
        delta_LDE = np.abs(LDE_flat - LDE_p) <= LDE_threshold
        delta_BD  = np.abs(BD_flat  - BD_p) <= BD_threshold

        F_count = front_mask.sum()
        NF_count = nonfront_mask.sum()

        P_front = 0.0
        P_nonfront = 0.0

        if F_count > 0:
            F_LDE_count = np.sum(front_mask & delta_LDE)
            F_BD_count  = np.sum(front_mask & delta_BD)
            P_front = (F_LDE_count / F_count) * (F_BD_count / F_count)

        if NF_count > 0:
            NF_LDE_count = np.sum(nonfront_mask & delta_LDE)
            NF_BD_count  = np.sum(nonfront_mask & delta_BD)
            P_nonfront = (NF_LDE_count / NF_count) * (NF_BD_count / NF_count)

        # Posterior decision
        if prior_p * P_front > (1.0 - prior_p) * P_nonfront:
            marked_matrix_out[idx] = 1
        else:
            marked_matrix_out[idx] = 0

    return marked_matrix_out

# ------------------------
# 主函数
# ------------------------
def bayesian_vectorized(marked_matrix, p10, p20, gradient_magnitude, SST):
    rows, cols = marked_matrix.shape

    # ------------------------
    # 1. Prior
    # ------------------------
    prior_matrix = np.ones_like(marked_matrix, dtype=np.float64)
    mask_nan = np.isnan(marked_matrix)
    mask2 = (marked_matrix == 2)
    prior_matrix[mask_nan] = np.nan
    prior_matrix[mask2] = (gradient_magnitude[mask2] - p20) / (p10 - p20)

    # ------------------------
    # 2. LDE and BD
    # ------------------------
    LDE, BD = compute_LDE_BD(SST)

    # ------------------------
    # 3. Flatten arrays
    # ------------------------
    marked_matrix_out = marked_matrix.copy().flatten().astype(np.uint8)
    grad_flat = gradient_magnitude.flatten()
    LDE_flat  = LDE.flatten()
    BD_flat   = BD.flatten()
    prior_flat = prior_matrix.flatten()

    idx_flat = np.flatnonzero(mask2.flatten() & ~mask_nan.flatten())

    # ------------------------
    # 4. Compute posterior
    # ------------------------
    marked_matrix_out = compute_posterior_batch(idx_flat, marked_matrix_out, prior_flat, LDE_flat, BD_flat, grad_flat, rows, cols)

    return marked_matrix_out.reshape(rows, cols)
