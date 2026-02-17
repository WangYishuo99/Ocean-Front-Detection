'''
Author: Yishuo Wang
Date: 2024-07-29 14:13:37
LastEditors: Yishuo Wang
LastEditTime: 2025-12-20 16:11:30
FilePath: /paper_detection/methods/GBM/main.py
Description: the main function for merge the results

Copyright (c) 2024 by Yishuo Wang, All Rights Reserved. 
'''
import get_date
import execution

import ray
import gc

start_time = '20250101'
end_time = '20250106'
input = './data'
output = './output_test'
types = ['SST', 'SSS']
start_lons = [100, 120]
end_lons = [125, 145]
start_lats = [0, 20]
end_lats = [25, 45]
region_names = ['SCS', 'KUR']

# 定义 Ray 远程任务（替代多进程）
@ray.remote
def ray_whole_function(*args):
    return execution.whole_function(*args)

if __name__ == '__main__':
    date_list = get_date.date_range(start_time, end_time)

    for type_now in types:
        for beginLon, endLon, beginLat, endLat, region_name in zip(start_lons, end_lons, start_lats, end_lats, region_names):
            
            # 启动 Ray（自动使用所有 CPU）
            ray.init()

            analysisType = 'phy'
            
            # 构建输入参数列表
            tasks = []
            for d in date_list:
                args = (
                    d, analysisType, input, output,
                    beginLon, endLon, beginLat, endLat, type_now, region_name
                )
                task = ray_whole_function.remote(*args)
                tasks.append(task)

            ray.get(tasks)

            ray.shutdown()

            # 保持串行循环内存精简，通过及时清理收集的对象。
            gc.collect()