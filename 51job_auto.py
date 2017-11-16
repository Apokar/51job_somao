# -*- coding: utf-8 -*-
# @Time         : 2017/11/16 10:56
# @Author       : Huaiz
# @Email        : Apokar@163.com
# @File         : 51job_auto.py
# @Software     : PyCharm Community Edition
# @PROJECT_NAME : 51job_somao

from sp27_51_all_2nd import *
from sp27_51_update import *

s_date = input('Start from (input like this : YYYYMMDD):')

while True:
    main_update(s_date)
    get_detail()

    timeArray = time.strptime(str(s_date), "%Y%m%d")
    # # 转换成时间戳
    timestamp = time.mktime(timeArray)

    timestamp = timestamp + int(345600)

    print timestamp
    if timestamp > int(time.time()):
        print u'已到最新,缓缓再爬.  '
        quit()
    else:
        time_local = time.localtime(timestamp)

        s_date = time.strftime("%Y%m%d", time_local)


        print u'现在爬' + s_date + '往后4天的内容'
