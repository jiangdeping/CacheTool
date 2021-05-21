# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/6 15:28
import os
filename =os.path.dirname(os.path.abspath(__file__))+ '\sup.txt'
LOG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log')
ThreadingNum=30 #设置线程数量