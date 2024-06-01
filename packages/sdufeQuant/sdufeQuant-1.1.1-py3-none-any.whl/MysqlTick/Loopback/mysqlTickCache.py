__author__ = 'zoulida'
#import tushare as ts
from rqalpha.environment import Environment
from rqalpha.utils.py2 import lru_cache
import pandas as pd
import datetime

def singleton(cls):
    instances = {}
    def getinstance(*args,**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args,**kwargs)
        return instances[cls]
    return getinstance

@singleton
class MyClass:
    a = 1



'''在上面，我们定义了一个装饰器 singleton，它返回了一个内部函数 getinstance，
该函数会判断某个类是否在字典 instances 中，如果不存在，则会将 cls 作为 key，cls(*args, **kw) 作为 value 存到 instances 中，
否则，直接返回 instances[cls]。'''

@singleton
class MysqlCache():

    def getLastTickPriceByEnvironment(self, rqcode):
        calendar_dt = Environment._env.calendar_dt
        date = calendar_dt.strftime("%Y-%m-%d")
        str_tick = calendar_dt.strftime("%H:%M:%S")
        import rqalpha.utilzld.zhengzeString as zz
        code = zz.getCode(rqcode)
        return self.getLastTickPrice(code, date, str_tick)

    def getLastTickPriceByDateTime(self, rqcode, calendar_dt):
        date = calendar_dt.strftime("%Y-%m-%d")
        str_tick = calendar_dt.strftime("%H:%M:%S")
        import rqalpha.utilzld.zhengzeString as zz
        code = zz.getCode(rqcode)
        return self.getLastTickPrice(code, date, str_tick)


    def getLastTickPrice(self, code, date, str_tick):
        price = self.getTickPrice(code, date, str_tick)
        while price is None:
            ticktime = datetime.datetime.strptime(str_tick, "%H:%M:%S")#时间倒退前进一秒,zoulida
            time_offset = ticktime - datetime.timedelta(seconds=1)
            str_tick =  time_offset.strftime("%H:%M:%S")
            price = self.getTickPrice(code, date, str_tick)
            if str_tick == "09:00:00":
                return None
            #print(str_tick)
        return price

    def getTickPrice(self, code, date, tick):
        records = self.getCacheData(code, date)
        #print(records['tick_time'] )
        recordone = records[records['tick_time'] == tick ]
        if recordone.empty :
            return None
        #print(recordone.iloc[0,5])
        return recordone.iloc[0,5]
        pass

    @lru_cache(maxsize = 16 * 1024 * 1024)
    def getdatafromMysql(self, code, date):#获取某一天的tick数据，并缓存在内存

        df = self.getdatafromshelve(code, date)
        '''import rqalpha.DBStock.dbQueryPools as dbpool
        #df = None
        df = dbpool.queryMySQL_tick_stock_market(code, date)
        #print(df)
        #df['date'] = pd.to_datetime(df['date'])
        #df.set_index('Date', inplace=True)
        #reslut = df[(True ^ df['close'].isin([0]))]  # 条件删除去除值为0的行'''

        return df

    def getdatafromshelve(self, code, date):
        import shelve
        name = code + '_' + str(date)
        print('shelve/TickData ', name)


        try:
            shelveDict = shelve.open('shelve/TickData')
        except Exception as e:
            print('出错，没有文件shelve/TickData。现在立即新建，并重复执行')
            import os
            os.makedirs('shelve')
            shelveDict = shelve.open('shelve/TickData')

        if name in shelveDict:
            listResult = shelveDict[name]
        else:
            # listResult = haveBeenGreaterThanbyOneDayCodelist(dateDay, percentage)
            import rqalpha.DBStock.dbQueryPools as dbpool
            listResult =  dbpool.queryMySQL_tick_stock_market(code, date)
            shelveDict[name] = listResult
        shelveDict.close()
        return listResult

    def getCacheData(self, code, date):
        '''enviroment = Environment.get_instance()
        startdata = enviroment.config.base.start_date
        import datetime
        startdata -= datetime.timedelta(days=365)#获取之前一年的数据，以备函数调用
        enddata = enviroment.config.base.end_date
        #print(startdata)'''
        data = self.getdatafromMysql(code, date)
        #print(data)
        #startstr = start.strftime('%Y-%m-%d')
        #endstr = end.strftime('%Y-%m-%d')
        #result = data.loc[start:end,]
        #result = data.loc[(data['date'] >= start) & (data['date'] <= end) ]
        #print(result)
        return data

if __name__ =='__main__':

    # c1 = MyClass()
    # c2 = MyClass()
    # print(c1 == c2) # True
    tc = MysqlCache()
    price = tc.getLastTickPrice('600016', '2019-06-06', '15:00:00')
    print(price)
    '''tc.getCacheData('000300', True, start ='2018-03-13', end = '2018-05-13')
    tc.getdatafromMysql('000300', True, start ='2018-03-13', end ='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tc.getdatafromMysql('000001', False, start='2018-03-13', end='2018-05-13')

    tb = MysqlCache().getdatafromMysql('000300', True, start='2018-03-13', end='2018-05-13')
    print(tb)'''

    pd = tc.getCacheData('600016', '2019-05-13')
    print(pd)

    price = tc.getTickPrice('600016', '2019-05-13', '09:25:05')
    print(price)

'''if __name__ == '__main__':
    ticktime = datetime.datetime.strptime('15:00:00', "%H:%M:%S")
    print(ticktime)
    #mtc = MysqlCache()
    #mtc.getLastTickPrice('600016', '2019-06-06', '15:00:00')'''