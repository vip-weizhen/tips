#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2022-3-16
Info: 定期向企业微信推送消息
cron: 20 7 * * *
new Env('天气预报');
"""
import requests
import re
import urllib.request
import json
import sys
import os
 
headers = {'Content-Type': 'application/json;charset=utf-8'}
##拷贝企业微信机器人生成的webhook
webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2af5db49-c10e-4d65-8acd-0aeb038a5502"
def msg(text):
    message= {
     "msgtype": "text",
        "text": {
            "content": text, ##注意后面跟【逗号】
	    "mentioned_list":["@all"] ##@群里所有人，可以不加
        },
        "at": {
            "isAtAll": True
        }
    }
    print(requests.post(webhook,json.dumps(message),headers=headers).content)
url = "https://tianqi.moji.com/weather/china/jiangsu/yuhuatai-district"    ##要爬取天气预报的网址(china后面是各个省市的地址)
par = '(<meta name="description" content=")(.*?)(">)' 
 
opener = urllib.request.build_opener()
urllib.request.install_opener(opener)
html = urllib.request.urlopen(url).read().decode("utf-8")
 
##提取需要爬取的内容
data = re.search(par,html).group(2)
msg(data)
