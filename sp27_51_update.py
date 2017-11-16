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

conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="51job", charset="utf8")
cursor = conn.cursor()

# cursor.execute('truncate table 51job_career_list')
# cursor.execute('truncate table 51job_career_detail')  # 清空数据库

data = []
main_urls = []
detail_urls = []
all_url = []


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

print '生成main_url  '+str(datetime.datetime.now())
for b in range(1, 6):
    for c in range(1, 7):
        for d in range(1, 8):
            for a in range(1, 13):
                if a < 10:
                    main_urls.append('http://search.51job.com/list/000000,000000,0000,00,9,' + '0' + str(
                        a) + ',%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=' + '0' + str(
                        b) + '&cotype=99&degreefrom=' + '0' + str(
                        c) + '&jobterm=99&companysize=' + '0' + str(
                        d) + '&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')

                else:
                    main_urls.append('http://search.51job.com/list/000000,000000,0000,00,9,' + str(
                        a) + ',%2B,2,1.html?lang=c&stype=1&postchannel=0000&workyear=' + '0' + str(
                        b) + '&cotype=99&degreefrom=' + '0' + str(
                        c) + '&jobterm=99&companysize=' + '0' + str(
                        d) + '&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=')
print '生成完毕  '+str(datetime.datetime.now())

def get_detail_urls():
    print 'get_detail 连接数据库 '+str(datetime.datetime.now())
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="51job", charset="utf8")
    cursor = conn.cursor()

    for url_first_page in main_urls:
        while True:
            try:
                soup_hp = BeautifulSoup(get_one_page(url_first_page), 'lxml')
                res_cooking = soup_hp.select('.og_but')
                get_num = res_cooking[1]
                num = re.findall('.*?onclick="jumpPage\(\'(.*?)\'\)', str(get_num))
                if num[0] == 1:
                    detail_urls.append(url_first_page)
                else:
                    for i in range(1, int(num[0]) + 1):
                        detail_urls.append(
                            url_first_page.split('.html')[0][:-1] + str(i) + '.html' + url_first_page.split('.html')[1])

                break
            except Exception, e:
                cursor.execute(
                    'insert into 51job_error_log values("%s","%s","%s","%s")' % (url_first_page, e, 'get_detail_urls错误 ',str(datetime.datetime.now())))
                conn.commit()
                print url_first_page + '再试一次 '+str(datetime.datetime.now())
                break
    return detail_urls


def get_data(detail_urls, s_date, e_date):
    ### 这一块为处理 获取的job_url是否之前有存在过，目前用此方法去重使得爬虫进程过于缓慢，先取消
    # print 'get_data 连接数据库 '+str(datetime.datetime.now())
    conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="51job", charset="utf8")
    cursor = conn.cursor()
    #
    # cursor.execute("SELECT a.job_url from 51job_career_list a union select b.url from 51job_error_log b")
    #
    # existed_url = cursor.fetchall()
    #
    # for old_urls in existed_url:
    #     for urls in old_urls:
    #         all_url.append(urls.encode('utf-8'))

    for url_hp in detail_urls:
        try:
            print 'getting 1st page  ' + url_hp
            soup_hp = BeautifulSoup(get_one_page(url_hp), 'lxml')
            res_cooking = soup_hp.select('div .el')
            # print res_cooking
            for i in range(10, len(res_cooking)):
                print 'HTML前 '+str(datetime.datetime.now())
                html = res_cooking[i].encode('latin1').decode('gbk')
                print 'HTML后 '+str(datetime.datetime.now())
                job_url = re_findall('class="t1 .*?">.*?<a href="(.*?)"', html)
                job_name = re_findall('.*?target="_blank" title="(.*?)">', html)
                company_url = re_findall('.*?class="t2"><a href="(.*?)"', html)
                company_name = re_findall('<span class="t2".*?target="_blank" title="(.*?)"', html)
                salary = re_findall('.*?class="t3">(.*?)</span>', html)
                lcation = re_findall('.*?"t4">(.*?)</span>', html)
                pub_date = re_findall('.*?"t5">(.*?)</span>', html)

                # 通过job_url在51job-career-list表和error表里找出都不在这之中的，才插入数据
                # if job_url not in all_url:

                # 增量补全数据时，在这里添加时间筛选条件
                # s_date和e_date的输入格式为  20170505
                # 先判断s_date和e_date是否跨年
                # 跨年的就按s_date到年底20xx1231和20xx0101到e_date处理
                if str(s_date)[:4] == str(e_date)[:4]:
                    print '检测出不跨年 '

                        # print str(time.localtime()[0]) + str(pub_date[0]).replace('-', '')
                    if str(s_date) <= str(time.localtime()[0]) + str(pub_date[0]).replace('-', '') <= str(e_date):
                        print '1-->' + pub_date[0]

                        # 插入时间符合的数据
                        cursor.execute(
                                'insert into 51job_career_list values ("%s","%s","%s","%s","%s","%s","%s","%s") ' % (
                                    job_url[0].split('?s=')[0], detag(job_name[0]), company_url[0], company_name[0],
                                    lcation[0],
                                    salary[0],
                                    pub_date[0], str(datetime.datetime.now())))
                        conn.commit()

                    else:
                        print '(1)当前处理的发布时间 不符合要求  ' + str(datetime.datetime.now())

                elif str(s_date)[:4] < str(e_date)[:4]:
                    if str(e_date)[4:] <= str(pub_date[0]).replace('-', '') <= str(
                                        time.localtime()[0] - 1) + '1231' and str(
                            time.localtime()[0]) + '0101' <= str(pub_date[0]).replace('-', '') <= str(e_date)[4:]:
                            # 插入时间符合的数据
                            print '2-->' + pub_date[0]
                            cursor.execute(
                                'insert into 51job_career_list values ("%s","%s","%s","%s","%s","%s","%s","%s") ' % (
                                    job_url[0].split('?s=')[0], detag(job_name[0]), company_url[0], company_name[0],
                                    lcation[0],
                                    salary[0],
                                    pub_date[0], str(datetime.datetime.now())))
                            conn.commit()
                    else:
                        print '(2)当前处理的发布时间 不符合要求  ' + str(datetime.datetime.now())
                else:
                    print '时间输入有误  '+str(datetime.datetime.now())


                    # data.append(detag(job_url[0].split('?s=')[0]))
                    # print '插入列表页---初级内容'
                # else :
                #     print '这条数据已存在数据库中 '+str(datetime.datetime.now())

        except Exception, e:
            if str(e).find('20006') >= 0:
                cursor.close()
                conn.close()
                conn = MySQLdb.connect(host="localhost", user="root", passwd="root", db="51job", charset="utf8")
                cursor = conn.cursor()
                print '数据库连接重启 '+str(datetime.datetime.now())

            elif str(e).find('10064') >= 0:
                print '插入数据错误 '+str(datetime.datetime.now())
                cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                job_url[0].split('?s=')[0], '10064', '1st_page', str(datetime.datetime.now())))
                conn.commit()
                print '错误信息 录入日志表 51job_error_log '+str(datetime.datetime.now())
            else:
                print '未知错误 '+str(datetime.datetime.now())
                cursor.execute('insert into 51job_error_log values("%s","%s","%s","%s")' % (
                job_url[0].split('?s=')[0], e, '1st_page', str(datetime.datetime.now())))
                conn.commit()


def main():
    detail_urls = get_detail_urls()
    print '输入时间范围    '+str(datetime.datetime.now())
    s_date = input('Start from (input like this : YYYYMMDD):')
    e_date = input('End time (input like this : YYYYMMDD):')
    get_data(detail_urls, s_date, e_date)
    # get_detail(data)


if __name__ == '__main__':
    main()
