'''
Author: Yishuo Wang
Date: 2024-07-19 12:54:59
LastEditors: Yishuo Wang
LastEditTime: 2025-12-20 15:40:23
Description: get the date between start and end and return a list
'''

# generate a list of dates between StartTime and EndTime, considering leap year and the end of month
def date_range(StartTime, EndTime):
    start_year = int(StartTime[0:4])
    end_year = int(EndTime[0:4])
    start_month = int(StartTime[4:6])
    end_month = int(EndTime[4:6])
    start_day = int(StartTime[6:8])
    end_day = int(EndTime[6:8])
    
    date_list = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            if year == start_year and month < start_month:
                continue
            if year == end_year and month > end_month:
                continue
            if month in [1, 3, 5, 7, 8, 10, 12]:
                days = 31
            elif month in [4, 6, 9, 11]:
                days = 30
            else:
                if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                    days = 29
                else:
                    days = 28
            for day in range(1, days + 1):
                if year == start_year and month == start_month and day < start_day:
                    continue
                if year == end_year and month == end_month and day > end_day:
                    continue
                date_list.append(year * 10000 + month * 100 + day)

    return date_list
