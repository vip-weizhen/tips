#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Create type_time: 2022-3-10
Info: 定期向企业微信推送消息
cron: 00 7 * * *
new Env('天气预报');
"""

import requests

headers = {
    'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
}

params = (
    ('style', 'tw'),
    ('skin', 'pitaya"'),
)

response = requests.get('https://tianqiapi.com/api.php', headers=headers, params=params)
send(response)
