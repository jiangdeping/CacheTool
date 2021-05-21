# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/19 9:38
from CacheTool.core.overWriteRequests import req
from CacheTool.conf.setting import ThreadingNum
import threading
sem=threading.Semaphore(ThreadingNum)
def flushSupplierCache(id):
    return req.get("http://192.168.10.35:12300/producer/user/go2/%s" % id, timeout=5)

def viewSupplierCache(id):
    return req.get("http://192.168.10.37:16100/go2.cn/cache/supplier/%s" % id, timeout=5)

def flushProductCache(id):
    with sem:
        return req.get("http://192.168.10.35:12300/producer/product/go2/%s" % id, timeout=5)

def viewProductCache(id):
    return req.get("http://192.168.10.37:16100/go2.cn/cache/product/%s" % id, timeout=5)