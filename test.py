#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

# for i in [1,2,3,4,5,6,7,'asd',8,9,10]:
#     try:
#         if i%2==0:
#             print i
#
#     except Exception, e:
#         print 'except'
lllist=[1,2,3,4,5,6,7,'asd',8,9,10]
def test():
    for i in lllist:
        if i%2==0:
            print i

if __name__ =="__main__":

    try:
        test()
    except Exception,e:
        print 'ooo'





