#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息
cron: 20 17 * * *
new Env('工作报备');
"""
import requests, json

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=2af5db49-c10e-4d65-8acd-0aeb038a5502"
send_message = "报备次日工作~"


def send_msg(content):
  data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)
  
send_msg(send_message)
send_msg(send_message)
send_msg(send_message)
