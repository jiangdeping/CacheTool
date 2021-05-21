# -*- coding: utf-8 -*-
# Author:jiang
# 2021/5/17 13:52
import logging
import os
from logging.handlers import TimedRotatingFileHandler
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(BASE_PATH, 'log')

class Logger():
    def __init__(self, loggername="DownLoadStory"):
        self.logger = logging.getLogger(loggername)
        self.logger.setLevel(logging.DEBUG)
        self.filename = os.path.join(LOG_PATH, "log")
        self.file_level = 'DEBUG'
        self.out_put_lever = "WARNING"
        self.format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                     datefmt='%Y/%m/%d %I:%M:%S %p')

    def get_logger(self):
        fh = TimedRotatingFileHandler(filename=self.filename, when='D', interval=1, backupCount=20,  # 最多保存的日志数
                                      delay=True, encoding='utf-8')
        fh.suffix = "%Y-%m-%d.log"
        fh.setLevel(self.file_level)
        fh.setFormatter(self.format)
        self.logger.addHandler(fh)
        ch = logging.StreamHandler()
        ch.setLevel(self.file_level)
        ch.setFormatter(self.format)
        self.logger.addHandler(ch)
        return self.logger


logger = Logger().get_logger()
# class Logger(object):
#     def __init__(self,logger_name='framework'):
#         self.logger=log.getLogger(logger_name)
#         log.root.setLevel(log.NOTSET)
#         self.log_file_name='log'
#         self.console_output_level="WARNING"
#         self.backup_count=5
#         self.file_output_level = 'DEBUG'
#         self.formatter = log.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt='%Y/%m/%d %I:%M:%S %p')
#         self.filename=os.path.join(LOG_PATH,self.log_file_name)
#     def get_logger(self):
#         """在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回"""
#         if not self.logger.handlers:  # 避免重复日志
#             # 控制台日志
#             console_handler = log.StreamHandler()
#             console_handler.setFormatter(self.formatter)
#             console_handler.setLevel(self.console_output_level)
#             self.logger.addHandler(console_handler)
#             # 每天重新创建一个日志文件，最多保留backup_count份
#             file_handler = TimedRotatingFileHandler(filename=self.filename,
#                                                     when='D',
#                                                     interval=1,
#                                                     backupCount=self.backup_count,#最多保存的日志数
#                                                     delay=True,
#                                                     encoding='utf-8'
#                                                     )
#             # 设置后缀名称，跟strftime的格式一样
#             file_handler.suffix="%Y-%m-%d.log"
#             # 文件日志
#             file_handler.setFormatter(self.formatter)
#             file_handler.setLevel(self.file_output_level)
#             self.logger.addHandler(file_handler)
#         return self.logger
# logger = Logger().get_logger()
