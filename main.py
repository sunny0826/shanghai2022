#!/usr/bin/env python
# encoding: utf-8
# Author: guoxudong
import pandas as pd
import requests
from jinja2 import Environment, FileSystemLoader

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
}
url = 'http://m.sh.bendibao.com/news/249468.html'
response = requests.get(url, headers=headers)
html_doc = str(response.content, 'utf-8')
df3 = pd.read_html(html_doc, encoding='utf-8')[0]
df3 = df3.drop([0, len(df3) - 1]).fillna(value=0)
df3.columns = df3.iloc[0]
df3['时间'] = df3['时间'].map('3月{}'.format)
df3['时间'] = df3['时间'] + df3['类型']
df3 = df3.drop(labels='类型', axis=1)
df3 = df3.drop([1])

url1 = 'http://m.sh.bendibao.com/news/250518.html'
response1 = requests.get(url1, headers=headers)
html_doc1 = str(response1.content, 'utf-8')
df4 = pd.read_html(html_doc1, encoding='utf-8')[0]
df4 = df4.drop([0, len(df4) - 1]).fillna(value=0)
df4.columns = df4.iloc[0]
df4['时间'] = df4['时间'].map('4月{}'.format)
df4['时间'] = df4['时间'] + df4['类型']
df4 = df4.drop(labels='类型', axis=1)
df4 = df4.drop([1])
df = pd.concat([df3, df4]).reset_index(drop=True)


def loopData(locals):
    arr = []
    for local in locals:
        arr.append(local)
    return arr


result = {}
result.update({'dates': loopData(df['时间'])})
result.update({'allData': loopData(df['合计'])})
result.update({'putuo': loopData(df['普陀'])})
result.update({'huangpu': loopData(df['黄浦'])})
result.update({'xuhui': loopData(df['徐汇'])})
result.update({'jingan': loopData(df['静安'])})
result.update({'hongkou': loopData(df['虹口'])})
result.update({'yangpu': loopData(df['杨浦'])})
result.update({'changning': loopData(df['长宁'])})
result.update({'pudong': loopData(df['浦东'])})
result.update({'jiading': loopData(df['嘉定'])})
result.update({'songjiang': loopData(df['松江'])})
result.update({'minghang': loopData(df['闵行'])})
result.update({'baoshan': loopData(df['宝山'])})
result.update({'qingpu': loopData(df['青浦'])})
result.update({'fengxian': loopData(df['奉贤'])})
result.update({'jinshan': loopData(df['金山'])})
result.update({'chongming': loopData(df['崇明'])})


def generate_html(data):
    env = Environment(loader=FileSystemLoader('./'))  # 加载模板
    template = env.get_template('template.html')
    # template.stream(body).dump('result.html', 'utf-8')

    with open("public/index.html", 'w') as fout:
        html_content = template.render(data)
        fout.write(html_content)  # 写入模板 生成html


generate_html(result)
