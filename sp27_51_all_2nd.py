#!/usr/bin/python
# -*- coding: utf-8 -*-


import datetime
import requests
import re
import MySQLdb
import mechanize

global br

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
cursor = conn.cursor()

#
# cursor.execute('truncate table 51job_career_detail')  # 清空表 51job_career_detail
# cursor.execute('truncate table 51job_error_log')  # 清空表 51job_error_log
data = []
main_urls = []
detail_urls = []


def get_one_page(url):
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            return response.text
        print 'url访问失败 ' + str(datetime.datetime.now())
        return None
    except:
        print 'url访问失败 ' + str(datetime.datetime.now())
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


def get_detail():
    print 'get_detail 连接数据库 ' + str(datetime.datetime.now())
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
    cursor = conn.cursor()
    print '提取2000数据 处理中 ' + str(datetime.datetime.now())
    cursor.execute(
        "select a.job_url from 51job_career_list a left join 51job_career_detail b on a.job_url=b.job_url left join 51job_error_log c on c.url=a.job_url where b.job_url is null and c.url is null limit 2000")
    print'获取 data 中 ' + str(datetime.datetime.now())
    data = cursor.fetchall()
    print'获得 data 啦 ' + str(datetime.datetime.now())

    for item in data:
        for sec_urls in item:
            try:
                print 'getting 2nd page  ' + sec_urls + '   ' + str(datetime.datetime.now())
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
                print 'html 前  ' + str(datetime.datetime.now())
                html = br.open(sec_urls).read().decode('gbk')
                print 'html 后  ' + str(datetime.datetime.now())
            except Exception, e:
                print sec_urls + ' --read网页出错'
                cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                    sec_urls, 'read网页出错,报错信息： ' + str(e), '2nd_page', str(datetime.datetime.now())))
                conn.commit()
                # break
            try:
                info = re_findall('class="msg ltype">(.*?)</p>', html)
                expr = re_findall('class="i1"></em>(.*?)</span>', html)
                edu = re_findall('class="i2"></em>(.*?)</span>', html)
                hire_number = re_findall('class="i3"></em>(.*?)</span>', html)
                label = re_findall('class="t2">.*?<span>(.*?)</p>', html)
                job_des = re_findall('class="bmsg job_msg inbox">.*?<span class="label">(.*?)<div class="mt10">', html)
                career_type = re_findall('<span class="el">(.*?)</span>', html)
                address = re_findall('<p class="fp">.*?<span class="label">.*?</span>(.*?)</p>', html)
                company_des = re_findall('class="tmsg inbox">(.*?)</div>', html)
            except Exception:
                print '该职位信息现已不存在导致的错误'

            try:
                cursor.execute(
                    'insert into 51job_career_detail values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") ' %
                    (
                        isExist(detag(info[0]).split('|')[0]),
                        isExist(detag(info[0]).split('|')[1]),
                        isExist(detag(info[0]).split('|')[2]),
                        expr[0],
                        edu[0],
                        hire_number[0],
                        detag(label[0].replace('</span>', '').replace('<span>', '|')),
                        detag(job_des[0]),
                        career_type[0],
                        address[0],
                        address[0],
                        detag(company_des[0]),
                        sec_urls
                    )

                )
                conn.commit()
                print '插入详情页--详细内容  ' + str(datetime.datetime.now())
            except Exception, e:
                if str(e).find('20006') >= 0:
                    cursor.close()
                    conn.close()
                    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="job", charset="utf8")
                    cursor = conn.cursor()
                    print '数据库连接重启  ' + str(datetime.datetime.now())

                elif str(e).find('10064') >= 0:
                    print sec_urls + ' --插入数据错误  ' + str(datetime.datetime.now())
                    cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                        sec_urls, '10064', '2nd_page', str(datetime.datetime.now())))
                    conn.commit()
                    print '错误信息 录入日志表 51job_error_log  ' + str(datetime.datetime.now())
                else:
                    print sec_urls + ' --出现未知错误  ' + str(datetime.datetime.now())
                    cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                        sec_urls, 'unknown', '2nd_page', str(datetime.datetime.now())))
                    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    while True:
        get_detail()
        print '2000条处理结束 ' + str(datetime.datetime.now())
