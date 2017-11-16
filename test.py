#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime
from multiprocessing import Pool

import requests
import re
import MySQLdb
from bs4 import BeautifulSoup
import mechanize
import time
global br

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

nowTime = int(time.time())

s_date = input('Start from (input like this : YYYYMMDD):')


# s_date = input('Start from (input like this : YYYYMMDD):')
timeArray = time.strptime(str(s_date), "%Y%m%d")
# 转换成时间戳
s_timestamp = time.mktime(timeArray)

e_timestamp = s_timestamp+int(345600)

print s_timestamp
print e_timestamp


pub_date = '10-20'
print str(s_date)[:4] + str(pub_date.replace('-',''))
