# -*- coding: utf-8 -*-
import sys
import getopt
import tarfile
import time
import re
import glob
import os


# 帮助函数
def helping():
    print sys.argv[0] + "-d 路径 -f 文件名前缀 -c log日志内容"
    print sys.argv[0] + "-h 获取帮助文档"


# 压缩log文件函数
def tar(fname):
    t = tarfile.open(fname + ".tar.gz", "w:gz")
    p, f = os.path.split(fname)
    os.chdir(p)
    t.add(f)
    t.close()


print "脚本名：", sys.argv[0]
# for i in range(1, len(sys.argv)):
# print "参数", i, sys.argv[i]

# hd:f:c:  ，表示命令的开头，h：帮助 ，d：log文件存储路径，f：log文件的前缀，c：log文件的内容
opts, args = getopt.getopt(sys.argv[1:], "hd:f:c:")

# 获取的变量内容，定义
path = ""
filePrefix = ""
content = ""

# 循环对变量进行赋值
for op, value in opts:
    if op == "-d":
        path = value
    elif op == "-f":
        filePrefix = value
    elif op == "-c":
        content = value
    elif op == "-h":
        helping()
        sys.exit()

# 时间模块，用于给log文件添加时间
# 设置时间格式
ISOTIMEFORMAT = "%Y-%m-%d"
timeNow = time.strftime(ISOTIMEFORMAT, time.localtime())

# Mac下的路径：/Users/tanishindaira/Desktop,Windows平台下，路径是不同的
# 通过字符串拼接,确定存储位置和文件名称
fileName = path + "/" + filePrefix + "-" + timeNow + ".log"

# 切割文件名，获取时间
filesNameSplit = path + r"/cms-*.log"
list = glob.glob(filesNameSplit)
cont = ""
for i in list:
    baseName = os.path.basename(i)
    cont += os.path.basename(i)
cut = re.split(r'(\W+)', cont)
# print cut
timeOld = cut[2] + cut[4] + cut[6]
# print timeOld


# 切割当前系统时间
cut1 = re.split(r'(\W+)', timeNow)
timeNowSplit = cut1[0] + cut1[2] + cut1[4]
# print timeNowSplit

# 判断时间，相等则写在当前文件内，不相等则单独写在新的文件内
if timeOld == timeNowSplit:
    # 写在当前文件
    f = file(fileName, "a")
    f.write(content + "\n")
    f.close
else:
    # 写在新文件里面
    f = file(fileName, "a")
    f.write(content + "\n")
    f.close

    # 将旧的log文件打包tar
    fileNameNew = path + "/" + cont
    tar(fileNameNew)

    # 删除旧的文件
    if os.path.exists(fileNameNew):
        os.remove(fileNameNew)

# 输出结果
print  "程序执行成功"
print path
print filePrefix
print content
