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

# cursor.execute('truncate table 51job_career_list')
# cursor.execute('truncate table 51job_career_detail')  # 清空数据库

data = []
main_urls = []
detail_urls = []
all_url=[]
# this_url='http://jobs.51job.com/shenzhen-ftq/66666666666.html'

def get_one_page(url):
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
        print 'url访问失败'
        return None
    except:
        print 'url访问失败'
        return None


def detag(html):
    detag = re.subn('<[^>]*>', ' ', html)[0]
    detag = detag.replace('&nbsp;', ' ')
    detag = detag.replace('&ensp;', ';')
    detag = detag.replace(' ', '')
    detag = detag.replace('\t', '')
    detag = detag.replace('\n', '')
    detag = detag.replace('\r', '')
    detag = detag.replace('"', '“')
    detag = detag.replace('\\', '')
    return detag


def re_findall(pattern, html):
    if re.findall(pattern, html, re.S):
        return re.findall(pattern, html, re.S)
    else:
        return 'N'


def isExist(object_item):
    if object_item:
        return object_item
    else:
        return 'Null'



    # def get_detail_urls():
    #     conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
    #     cursor = conn.cursor()

    # url_first_page = 'http://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    #
    # soup_hp = BeautifulSoup(get_one_page(url_first_page), 'lxml')
    # res_cooking = soup_hp.select('.og_but')
    # get_num = res_cooking[1]
    # num = re.findall('.*?onclick="jumpPage\(\'(.*?)\'\)', str(get_num))
    # if num[0] == 1:
    #     detail_urls.append(url_first_page)
    # else:
    #     for i in range(1, int(num[0]) + 1):
    #         detail_urls.append(
    #             url_first_page.split('.html')[0][:-1] + str(i) + '.html' + url_first_page.split('.html')[1])
    #
    # print detail_urls


def get_data():
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT a.job_url from aaa a union select b.job_url from bbb b")

    existed_url = cursor.fetchall()

    for old_urls in existed_url:
        for urls in old_urls:
            all_url.append(urls.encode('utf-8'))


    # if this_url not in  all_url:
    #     print 'haha'


    # url_hp='http://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    #
    # print 'getting 1st page  ' + url_hp
    # soup_hp = BeautifulSoup(get_one_page(url_hp), 'lxml')
    # res_cooking = soup_hp.select('div .el')
    # # print res_cooking
    # for i in range(10, len(res_cooking)):
    #     html = res_cooking[i].encode('latin1').decode('gbk')
    #     job_url = re_findall('class="t1 .*?">.*?<a href="(.*?)"', html)
    #
    #     # 第一步
    #     cursor.execute(
    #
    #         'insert into aaa values ("%s") ' % (
    #             job_url[0].split('?s=')[0]))
    #     conn.commit()
        # 第二布
        # if job_url not in existed_url:
        #     cursor.execute(
        #         'insert into ccc values ("%s") ' % (
        #             job_url[0].split('?s=')[0]))
        #     conn.commit()
        #     print '补全一条数据成功'
        # else:
        #     print '已存在的数据跳过'


def main():
    # detail_urls = get_detail_urls()
    get_data()
    # get_data(detail_urls)
    # get_detail(data)


if __name__ == '__main__':
    main()
