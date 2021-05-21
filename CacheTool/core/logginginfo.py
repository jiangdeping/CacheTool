# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/17 16:26

import logging
import time

class MyLogHandler(logging.Handler):
    def __init__(self,obj):
        logging.Handler.__init__(self)
        logging.basicConfig(level=logging.INFO)
        self.Object = obj
    def emit(self,record):
        tstr = time.strftime('%Y-%m-%d_%H:%M:%S.%U')
        self.Object.AppendText("[%s][%s] %s\n"%(tstr,"--初始化数据--",record.getMessage()))