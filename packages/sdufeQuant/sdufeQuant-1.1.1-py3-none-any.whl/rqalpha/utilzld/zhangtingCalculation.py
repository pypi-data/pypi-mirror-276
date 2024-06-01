__author__ = 'zoulida'

def limitUp(close):
    lup = round(close * 110) /100.0 #只用round结果不符合四舍五入的规则。为什么会这样呢？原因是：round()函数只有一个参数，不指定位数的时候，返回一个整数，而且是最靠近的整数，类似于四舍五入，当指定取舍的小数点位数的时候，一般情况也是使用四舍五入的规则，但是碰到.5的情况时，如果要取舍的位数前的小数是奇数，则直接舍弃，如果是偶数则向上取舍。
    return lup

def limitDown(close):
    ldown = round(close * 90) / 100.0
    return ldown

def STlimitUp(close):
    return

def STlimitDown(close):
    return

if __name__ == '__main__':
    tt = limitUp(18.25)
    print(tt)