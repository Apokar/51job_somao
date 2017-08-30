#!/usr/bin/python
# -*- coding: utf-8 -*-
import datetime

for i in [1,2,3,4,5,6,7,'asd',8,9,10]:
    while True:
        try:
            i%2==0
            print i
            break
        except Exception, e:
            print 'except'
            break
