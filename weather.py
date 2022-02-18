# -*- coding: utf-8 -*-
"""
cron: 30 7 * * *
new Env('天气预报');
"""

import requests

import re

import urllib.request

import json

import sys

import os

headers = {'Content-Type': 'application/json;charset=utf-8'}


webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37e7e521-28b2-4064-b572-8effb4071d6a"

def msg(text):

message= {undefined

"msgtype": "text",

"text": {undefined

"content": text, 

"mentioned_list":[""] 

},

"at": {undefined

"isAtAll": True

}

}

print(requests.post(webhook,json.dumps(message),headers=headers).content)

url = "https://tianqi.moji.com/tommorrow/china/jiangsu/nanjing" 

par = '()'

opener = urllib.request.build_opener()

urllib.request.install_opener(opener)

html = urllib.request.urlopen(url).read().decode("utf-8")


data = re.search(par,html).group(2)

msg(data)
