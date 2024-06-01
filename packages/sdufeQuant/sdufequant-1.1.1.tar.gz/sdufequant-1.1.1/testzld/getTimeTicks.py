__author__ = 'zoulida'

# -*- coding=utf-8 -*-
import warnings
import datetime

warnings.filterwarnings("ignore")


def getNowDay():
    DayNow = datetime.datetime.today().strftime('%Y-%m-%d')
    return DayNow


def getYesterDay():
    YesterDay = (datetime.datetime.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')
    return YesterDay


def dateRange(beginDate, endDate):
    dates = []
    dt = datetime.datetime.strptime(beginDate, "%Y-%m-%d")
    date = beginDate[:]
    while date <= endDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y-%m-%d")
    return dates


def monthRange(beginDate, endDate):
    monthSet = set()
    for date in dateRange(beginDate, endDate):
        monthSet.add(date[0:7])
    monthList = []
    for month in monthSet:
        monthList.append(month)
    return sorted(monthList)


def dateHourRange(beginDateHour, endDateHour):
    dhours = []
    dhour = datetime.datetime.strptime(beginDateHour, "%Y-%m-%d %H")
    date = beginDateHour[:]
    while date <= endDateHour:
        dhours.append(date)
        dhour = dhour + datetime.timedelta(hours=1)
        date = dhour.strftime("%Y-%m-%d %H")
    return dhours

def dateSecondRange(beginDateSecond, endDateSecond):
    seconds = []
    second = datetime.datetime.strptime(beginDateSecond, "%Y-%m-%d %H:%M:%S")
    time = beginDateSecond[:]
    while time <= endDateSecond:
        seconds.append(time)
        second = second + datetime.timedelta(seconds=1)
        time = second.strftime("%Y-%m-%d %H:%M:%S")
    return seconds

# print(getNowDay())
#
# print(getYesterDay())
#
# print(dateRange(beginDate='2018-06-05', endDate='2018-07-09'))
#
# print(monthRange(beginDate='2018-01-09', endDate='2019-09-01'))

#print(dateHourRange(beginDateHour='2018-01-01 23', endDateHour='2018-01-03 00'))

print(dateSecondRange(beginDateSecond='2018-01-01 23:00:00', endDateSecond='2018-01-03 00:00:00'))