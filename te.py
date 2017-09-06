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

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
cursor = conn.cursor()

cursor.execute("SELECT a.url from 51job_error_log a  ")
url = cursor.fetchall()
print '输入时间范围'+str(datetime.datetime.now())