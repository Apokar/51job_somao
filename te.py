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

import logging
import sys

s_date = input('Start from (input like this : YYYYMMDD):')

while True:
    timeArray = time.strptime(str(s_date), "%Y%m%d")
            # # 转换成时间戳
    timestamp = time.mktime(timeArray)

    timestamp = timestamp + int(345600)

    print timestamp
    if timestamp < int(time.time()):

        time_local = time.localtime(timestamp)

        s_date = time.strftime("%Y%m%d", time_local)

        print s_date
        time.sleep(3)
    else:
        quit()