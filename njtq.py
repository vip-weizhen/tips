#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2022-3-10
Info: 定期向企业微信推送消息
cron: 00 7 * * *
new Env('天气预报');
"""

import requests, json
wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37e7e521-28b2-4064-b572-8effb4071d6a"
def send_msg(content):
  data = json.dumps({"msgtype": "news", "articles": [{"url":"https://tianqiapi.com/api.php?style=tw&skin=pitaya"}]})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)
send_msg(print)
