#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author  :hstking
# E-mail  :hstking@hotmail.com
# Ctime   :2015/09/15
# Mtime   :
# Version :

import logging
import getpass
import sys


#### 定义MyLog类
class MyLog(object):
    #### 类MyLog的构造函数
    def __init__(self):
        # 获取用户名称
        self.user = getpass.getuser()
        # log记录表明用户
        self.logger = logging.getLogger(self.user)
        # log 等级
        self.logger.setLevel(logging.DEBUG)
        ####  日志文件名
        self.logFile = sys.argv[0][0:-3] + '.log'
        # log文件格式
        self.formatter = logging.Formatter('%(asctime)-12s %(levelname)-8s %(name)-10s %(message)-12s\r\n')
        ####  日志输出到日志文件内
        self.logHand = logging.FileHandler(self.logFile, encoding='utf8')
        self.logHand.setFormatter(self.formatter)
        self.logHand.setLevel(logging.DEBUG)
        # 日志显示到屏幕
        self.logHandSt = logging.StreamHandler()
        self.logHandSt.setFormatter(self.formatter)
        self.logHandSt.setLevel(logging.DEBUG)

        self.logger.addHandler(self.logHand)
        self.logger.addHandler(self.logHandSt)

    ####  日志的5个级别对应以下的5个函数
    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warn(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)
