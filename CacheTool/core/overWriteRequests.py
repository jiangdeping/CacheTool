# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/6 9:48
import requests
from requests import  adapters
def overWriteRequests():
    requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
    s = requests.session()
    s.keep_alive = False  # 关闭多余连接
    return requests
req=overWriteRequests()