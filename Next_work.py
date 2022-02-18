#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息
cron: 20 17 * * *
new Env('工作报备');
"""
import requests, json
import datetime
import time

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37e7e521-28b2-4064-b572-8effb4071d6a"  # 测试机器人1号
send_message = "测试：测试机器人1号………………………………！"


def send_msg(content):
  """艾特全部，并发送指定信息"""
  data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@all"]}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)