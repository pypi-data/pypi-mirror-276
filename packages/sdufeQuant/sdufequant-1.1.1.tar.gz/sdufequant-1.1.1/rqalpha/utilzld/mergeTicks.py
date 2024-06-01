__author__ = 'zoulida'
__author__ = 'zoulida'
import rqalpha.utilzld.secondsList as secondsList
import datetime


def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class MergeTicks():
    daysofTick = {}
    beginTime = "09:25:00"  # 写到config
    endTime = "15:00:30"


    breakBeginTime = "11:30:05" #  中午休息
    breakEndTime = "13:00:00"

    def setBeginTime(self, beginTime):
        self.beginTime = beginTime
    def setEndTime(self, endTime):
        self.endTime = endTime
    def getDatString(self, trading_date):
        data1str = trading_date.strftime("%Y-%m-%d")
        return data1str

    def munisTicks(self, trading_date_str, elTicks):

        ticks = self.getTicksbyStrDay(trading_date_str)

        list = [i for i in ticks if i not in elTicks]
        self.daysofTick[trading_date_str] = list

    def getTicksbyStrDay(self, trading_date_str):
        if self.daysofTick.get(trading_date_str) is not None:
            return self.daysofTick.get(trading_date_str)
        else:
            self.daysofTick[trading_date_str] = self.get_merge_ticks(trading_date_str)
            return self.daysofTick[trading_date_str]

    def getTicks(self, trading_date):
        trading_date_str = trading_date.strftime("%Y-%m-%d")
        return self.getTicksbyStrDay(trading_date_str)

    def deleteOneTick(self, trading_date, tick):
        trading_date_str = trading_date.strftime("%Y-%m-%d")
        ticks = self.getTicksbyStrDay(trading_date_str)
        ticks.remove(tick)
        self.daysofTick[trading_date_str] = ticks

    def hasNextTick(self, trading_date):
        ticks = self.getTicks(trading_date)
        if len(ticks) > 0:
            return True
        else:
            return False




    def get_merge_ticks(self, trading_date_str):

        from rqalpha.utilzld.secondsList import dateSecondRangeByDatatime

        #data1str = trading_date.strftime("%Y-%m-%d")

        dataBeginTimestr = trading_date_str + " " + self.beginTime
        dataEndTimestr = trading_date_str + " " + self.endTime
        breakBeginTimestr = trading_date_str + " " + self.breakBeginTime
        breakEndTimestr = trading_date_str + " " + self.breakEndTime
        #import datetime
        dataBeginTime = datetime.datetime.strptime(dataBeginTimestr, "%Y-%m-%d %H:%M:%S")
        breakBeginTime = datetime.datetime.strptime(breakBeginTimestr, "%Y-%m-%d %H:%M:%S")
        listTicksMorning = dateSecondRangeByDatatime(dataBeginTime, breakBeginTime)

        dataEndTime = datetime.datetime.strptime(dataEndTimestr, "%Y-%m-%d %H:%M:%S")
        breakEndTime = datetime.datetime.strptime(breakEndTimestr, "%Y-%m-%d %H:%M:%S")
        listTicksafternoon = dateSecondRangeByDatatime(breakEndTime, dataEndTime)

        listTicks = listTicksMorning + listTicksafternoon
        #print(listTicks)
        return listTicks
        # print(listTicks)



if __name__ == '__main__':
    s_date = datetime.datetime.strptime("2016-06-07", "%Y-%m-%d")
    mt = MergeTicks()
    ticks = mt.getTicksbyStrDay("2016-06-07")
    #print(ticks)

    import rqalpha.utilzld.eliminateTicks as et
    el = et.ELiminateTicks()
    el.addTicksbyString('2016-06-07 14:51:00', '2016-06-07 14:59:00')
    elticks = el.getELTicks()
    #print(el.getELTicks())

    import time
    start = time.time()
    mt.munisTicks("2016-06-07", elticks)
    ticks2 = mt.getTicksbyStrDay("2016-06-07")
    stop = time.time()
    print('delay: %.3fs' % (stop - start))


    print(ticks2)

    '''el = ELiminateTicks()
    el.addTicksbyString('2019-08-08 14:51:00', '2019-08-08 14:52:00')
    print(el.getELTicks())'''