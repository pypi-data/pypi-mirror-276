__author__ = 'zoulida'


#获取当天涨停以及几乎涨停的股票list，其中percentage是指最高价的涨幅。为了避免每次在数据库所有表中搜索当天数据，所以采用shelve的方法将中间结果放入磁盘。

from santai3.tools.tusharePro import getPro
from santai3.tools.LogTools import Logger
import time
logger = Logger(logName='log.txt', logLevel="DEBUG", logger="santai3").getlog()
#from tools.connectMySQL import getStockDataBaseCursorAndDB

def getProOk():#没有用到
    getPro()
def getZTList(codelist, dateDay):
    listA = []
    #if haveBeenGreaterThanbyOneDay(codelist, dateDay):
    #    listA.append(code)
def getGreaterThanList(dateDay, percentage = 1.07):#取得最高价大于percentage的list

    import shelve
    name = dateDay + '_' +str(percentage)
    print(name)
    shelveDict = shelve.open('shelve/scanZToneDay3')
    if name in shelveDict:
        listResult = shelveDict[name]
    else:
        #listResult = haveBeenGreaterThanbyOneDayCodelist(dateDay, percentage)
        listResult = haveBeenGreaterThanbyOneDayRemoveOpenLimitUp_Codelist(dateDay, percentage)

        shelveDict[name] = listResult
    shelveDict.close()
    return listResult

def addList(res_l):
    for res in res_l:
        #spend = (timest - datetime.datetime.now()).total_seconds()
        #time = datetime.datetime.now()
        #print('正在提取结果：  ', listtemp5.__len__(),'   ; 上次消耗时间 ' , spend)
        try:
            item = res.get()
        except Exception as e:
            print('traceback.print_exc():', e)
            import traceback
            traceback.print_exc()

def haveBeenGreaterThanbyOneDayRemoveOpenLimitUp_Codelist(dateDay ,percentage):#涨停股票，去除一字涨停
    import santai3.tools.connectMySQL as CL
    cursor, db = CL.getStockDataBaseCursorAndDB()
    # start_date = None
    start = time.time()
    listResult = []
    codelist = getStockList()

    try:
        start = time.time()
        for row in codelist.itertuples(index=True, name='Pandas'):
            code = getattr(row, "Index")
            sqlSentence = "SELECT * FROM stockdatabase.stock_%s where 日期 =  \'%s\' and 最高价 > %s * 前收盘  and round(开盘价,2)  != round(round(前收盘 * 110)/100,2)" % (
            code, dateDay, percentage) #这里要注意开盘价是float，比较越来有误差，因此要加round
            print(sqlSentence)

            cursor.execute(sqlSentence)
            results = cursor.fetchone()
            print(results)
            if results is not None:
                # return True
                # print(True)
                listResult.append(code)

        stop = time.time()
        print('delay: %.3fs' % (stop - start))
    except Exception as msg:
        # print(str(msg))
        logger.error(msg)
    finally:
        # 关闭游标，提交，关闭数据库连接
        cursor.close()
        db.commit()
        db.close()
    return listResult
def haveBeenGreaterThanbyOneDayCodelist(dateDay ,percentage):
    import santai3.tools.connectMySQL as CL
    cursor, db = CL.getStockDataBaseCursorAndDB()
    #start_date = None
    start = time.time()
    listResult = []
    codelist = getStockList()

    try:
        start = time.time()
        for row in codelist.itertuples(index=True, name='Pandas'):
            code = getattr(row, "Index")
            sqlSentence = "SELECT * FROM stockdatabase.stock_%s where 日期 =  \'%s\' and 最高价 > %s * 前收盘 "  % (code, dateDay, percentage)
            print(sqlSentence)

            cursor.execute(sqlSentence)
            results = cursor.fetchone()
            print(results)
            if results is not None:
                #return True
                #print(True)
                listResult.append(code)

        stop = time.time()
        print('delay: %.3fs' % (stop - start))
    except Exception as msg:
        #print(str(msg))
        logger.error(msg)
    finally:
        # 关闭游标，提交，关闭数据库连接
        cursor.close()
        db.commit()
        db.close()
    return listResult

def haveBeenGreaterThanbyOneDay(code, dateDay ,percentage):
    import santai3.tools.connectMySQL as CL
    cursor, db = CL.getStockDataBaseCursorAndDB()
    #start_date = None
    try:
        sqlSentence = "SELECT * FROM stockdatabase.stock_%s where 日期 =  \'%s\' and 最高价 > %s * 前收盘 "  % (code, '2017-09-04', percentage)
        print(sqlSentence)

        cursor.execute(sqlSentence)

        results = cursor.fetchone()
        print(results)
        if results is not None:
            return True

    except Exception as msg:
        #print(str(msg))
        logger.error(msg)
    finally:
        # 关闭游标，提交，关闭数据库连接
        cursor.close()
        db.commit()
        db.close()
    return False

def getStockList():
    from santai3.tools.StockList import get_all_stock2
    codelist = get_all_stock2()
    return codelist

def poolpre():
    from multiprocessing import Pool, Manager
    from multiprocessing import cpu_count
    #print(cpu_count())
    pool = Pool(100)
    #pool = Pool(cpu_count()+2)
    return pool





percentage = 1.07  #1.07 代表上涨%7以上

if __name__ == '__main__':
    #import datetime
    #print(datetime.datetime.today())

    #codelist = getStockList()

    #code = ""
    dateDay = '2017-09-06'
    #getGreaterThanList(codelist, dateDay)
    listResult = getGreaterThanList(dateDay)
    #listResult = getGreaterThanList(dateDay , percentage)

    print(listResult)