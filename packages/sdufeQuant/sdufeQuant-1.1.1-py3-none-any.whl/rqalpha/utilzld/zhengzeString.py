__author__ = 'zoulida'

import re

def getCode(rqCode):
    pattern = r'[.]'
    code = re.split(pattern, rqCode)[0]
    #print(code)
    return code

if __name__ == '__main__':
    getCode("600519.XSHG")