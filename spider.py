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


#cursor.execute('truncate table 51job_test')
# cursor.execute('truncate table 51job_career_test2')  # 清空数据库

data = []
main_urls = []
detail_urls = []


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
    detag = detag.replace('\\','')
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

def get_detail(sec_urls):
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
    cursor = conn.cursor()
    # cursor.execute("select a.job_url from 51job_tt a left join (select * from 51job_career_test2) b on a.job_url=b.job_url where b.job_url is null limit 500")
    # data = cursor.fetchall()
    # print data


    try:
        print 'getting 2nd page  ' + sec_urls
        br = mechanize.Browser()
        br.addheaders = [
                            ('User-agent',
                             'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36') \
                            , ('Accept-Language', 'zh-CN,zh;q=0.8') \
                            , ('Accept-Encoding', 'gzip, deflate, sdch') \
                            , ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8') \
                            , ('Cache-Control', 'max-age=0') \
                            , ('Referer', 'http://biz.163.com/') \
                            , ('Connection', 'keep-alive') \
                            , ('Content-Type', 'application/x-www-form-urlencoded; charset=gbk') \
                            , ('Upgrade-Insecure-Requests', '1') \
                            ]

        html = br.open(sec_urls).read().decode('gbk')
    except Exception,e:
        print sec_urls+' --read网页出错'
        cursor.execute('insert into 51job_error_log222 values("%s","%s","%s","%s")' % (sec_urls, 'read网页出错,报错信息： '+str(e), '2nd_page',str(datetime.datetime.now())))
        conn.commit()
                    # print html
    info = re_findall('class="msg ltype">(.*?)</p>', html)
    expr = re_findall('class="i1"></em>(.*?)</span>', html)
    edu = re_findall('class="i2"></em>(.*?)</span>', html)
    hire_number = re_findall('class="i3"></em>(.*?)</span>', html)
    label = re_findall('class="t2">.*?<span>(.*?)</p>', html)
    job_des = re_findall('class="bmsg job_msg inbox">.*?<span class="label">(.*?)<div class="mt10">', html)
    career_type = re_findall('<span class="el">(.*?)</span>', html)
    address = re_findall('<p class="fp">.*?<span class="label">.*?</span>(.*?)</p>', html)
    company_des =re_findall('class="tmsg inbox">(.*?)</div>', html)


    try:
        cursor.execute(
                'insert into 51job_career_test2 values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") ' %
                    (
                                isExist(detag(info[0]).split('|')[0]),
                                isExist(detag(info[0]).split('|')[1]),
                                isExist(detag(info[0]).split('|')[2]),
                                expr[0],
                                edu[0],
                                hire_number[0],
                                detag(label[0].replace('</span>', '').replace('<span>', '|')),
                                detag(job_des[0]),
                                career_type,
                                address[0],
                                address[0],
                                detag(company_des[0]),
                                sec_urls
                    )

        )
        conn.commit()
        print '插入详情页--详细内容'
    except Exception,e:
        if str(e).find('20006') >= 0:
            cursor.close()
            conn.close()
            conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
            cursor = conn.cursor()
            print '数据库连接重启'

        elif str(e).find('10064') >= 0:
            print sec_urls+' --插入数据错误'
            cursor.execute('insert into 51job_error_log222 values("%s","%s","%s","%s")' % (sec_urls, '10064','2nd_page',str(datetime.datetime.now())))
            conn.commit()
            print '错误信息 录入日志表 51job_error_log'
        else:
            print sec_urls+' --出现未知错误'
            cursor.execute('insert into 51job_error_log222 values("%s","%s","%s","%s")' % (sec_urls, 'unknown','2nd_page',str(datetime.datetime.now())))
            conn.commit()
    cursor.close()
    conn.close()

if __name__=='__main__':
    while True:
        get_detail()
        print '500条处理结束 '
        time.sleep(0.5)
        print '休息0.5秒'