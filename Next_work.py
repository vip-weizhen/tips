#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息
cron: 20 17 * * *
new Env('工作报备');
"""
import requests, json

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37e7e521-28b2-4064-b572-8effb4071d6a"
send_message = "测试测试测试测试测试测试测试测试测试测试测试"


def send_msg(content):
  data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)
  
send_msg(send_message)
