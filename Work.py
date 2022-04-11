#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2022-4-8
Info: 定期向企业微信推送消息
cron: 0 0-23/1 * * *
new Env('待派工任务');
"""
import requests, json
let content = []

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37e7e521-28b2-4064-b572-8effb4071d6a"


def send_msg(content):
  data = json.dumps({"msgtype": "markdown", "markdown": {"content":content}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)
  
send_msg(content)
