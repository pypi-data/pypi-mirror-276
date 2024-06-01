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
class ELiminateTicks():
    seconds = []
    def getELTicks(self):
        return self.seconds
    def cleanTicks(self):
        self.seconds = []
    def addTicks(self, seconds):
        self.seconds.extend(seconds)#append(seconds) append() 追加单个元素到List的尾部，只接受一个参数，参数可以是任何数据类型，被追加的元素在List中保持着原结构类型。,extend() 将一个列表中每个元素分别添加到另一个列表中，只接受一个参数。
        pass
    def removeTicks(self):
        pass
    def addTicksFromBingeToEnd(self, beginDateSecond, endDateSecond):
        seconds = secondsList.dateSecondRangeByDatatime(beginDateSecond, endDateSecond)
        self.addTicks(seconds)
    def addTicksbyString(self, beginDateSecondstr, endDateSecondstr):

        beginDateSecond = datetime.datetime.strptime(beginDateSecondstr, "%Y-%m-%d %H:%M:%S")
        endDateSecond = datetime.datetime.strptime(endDateSecondstr, "%Y-%m-%d %H:%M:%S")
        self.addTicksFromBingeToEnd(beginDateSecond, endDateSecond)

if __name__ == '__main__':
    el = ELiminateTicks()
    el.addTicksbyString('2019-08-08 14:51:00', '2019-08-08 14:52:00')
    print(el.getELTicks())