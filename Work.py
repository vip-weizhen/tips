#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2020-2-24
Info: 定期向企业微信推送消息
cron: 0 0-23/1 * * *
new Env('工作任务发布');
"""
import requests, json

wx_url = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=37e7e521-28b2-4064-b572-8effb4071d6a"
1 = "南京江北扬子科创三期  科拓  3进3出  南京市浦口区腾飞大厦旁"
2 = "南京金叶花园  科拓  1进1出  南京市雨花台区龙飞路8号"


def send_msg(content):
  data = json.dumps({"msgtype": "text", "text": {"content": content, "mentioned_list":["@"]}})
  r = requests.post(wx_url, data, auth=('Content-Type', 'application/json'))
  print(r.json)
  
send_msg(1,2)

