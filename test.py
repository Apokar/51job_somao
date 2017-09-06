#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

for i in [1,2,3,4,5,6,7,'asd',8,9,10]:
    try:
        if i%2==0:
            print i
            time.sleep(3)
    except Exception, e:
        print 'except'





