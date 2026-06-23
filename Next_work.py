#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息
cron: 20 17 * * *
new Env('工作报备');
"""
import requests, json, time

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="
send_message = "报备次日工作计划~"


def send_msg(content):
  data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)
  
send_msg(send_message)
time.sleep(5)
send_msg(send_message)
time.sleep(5)
send_msg(send_message)
time.sleep(1200)
send_msg(send_message)
time.sleep(1200)
send_msg(send_message)

