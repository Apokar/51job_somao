import json
from multiprocessing.pool import Pool

import pymysql
import re
import urllib.request

conn = pymysql.connect(host='localhost', user='root', passwd='root', db='job', charset='utf8')
cursor = conn.cursor()
sql = "select * from 51job_test"
urls=[]
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
    title_url = row[1]
    company_url = row[3]
    urls.append(title_url)


# def get_sec_page(url):
#
#     a = urllib.request.urlopen(url)
#     html = a.read()
#     html = html.decode('gbk')
#     return html
#     print(html)


def parse_page(url):
    print('111')
    reg = re.compile(
        r'class="msg ltype">(.*?)&nbsp;&nbsp;|&nbsp;&nbsp;(.*?)&nbsp;&nbsp;|&nbsp;&nbsp;(.*?)</p>.*?<em class="i1"></em>(.*?)'
        r'</span>.*?<em class="i2"></em>(.*?)</span>.*?<em class="i3"></em>(.*?)</span>.*?<p class="t2"><span>(.*?)</span></p>.*?'
        r'职位描述：</span>(.*?)<div class="mt10"><p class="fp f2"><span class="label">职能类别：.*?<span class="el">(.*?)</span></p>'
        r'.*?上班地址：</span>(.*?)</p><a class="icon_b.*?<div class="tmsg inbox">(.*?)</div></div>',re.S
    )
    items = re.findall(reg,url)

    for item in items:
        yield {
            'company_type':item[0],
            'scale':item[1],
            'industry':item[2],
            'exper':item[3],
            'edu':item[4],
            'hire_number': item[5],
            'label': item[6].replace('<span>','').replace('</span>','|'),
            'job_description': item[7],
            'career_type': item[8],
            'address': item[9],
            'company_address':item[9],
            'company_description': item[10]
        }

        cursor.execute('insert into 51job_career_test2 values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s") ' % (
            item[0], item[1], item[2], item[3], item[4], item[5], item[6],item[7],item[8],item[9],item[9],item[10]))
        conn.commit()
        print('cha ru')

def write_to_file(content):
    with open('record222.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


# def main(url):
#     for item in parse_page(url):
#         write_to_file(item)

if __name__ == '__main__':
    for url in urls:

