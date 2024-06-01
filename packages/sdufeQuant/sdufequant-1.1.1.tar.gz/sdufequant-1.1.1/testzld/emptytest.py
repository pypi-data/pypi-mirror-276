__author__ = 'zoulida'

import numpy as np
arr = np.empty([2,2])
print(arr)


import sys
import os

print( "当前工作路径",os.getcwd())
sys.path.append("/volume/pythonworkspace")
print(sys.path)
import sdufeQuant.rqalpha.const