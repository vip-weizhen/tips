#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests
import re

# 替换成你的新webhook地址
webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="

def send_wechat_msg(content):
    """发送消息到企业微信"""
    message = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_list": []
        }
    }
    try:
        result = requests.post(webhook, json=message)
        print(f"发送结果: {result.json()}")
        if result.json().get('errcode') == 0:
            print("发送成功")
        else:
            print(f"发送失败: {result.json()}")
    except Exception as e:
        print(f"请求异常: {e}")

# 目标网址
url = "https://tianqi.moji.com/weather/china/jiangsu/yuhuatai-district"

# 伪装成浏览器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    html = response.text
    
    # 直接从meta标签提取天气信息（更稳定）
    desc_match = re.search(r'<meta name="description" content="(.*?)">', html)
    
    if desc_match:
        # meta description里包含了完整的天气信息
        weather_info = f"南京雨花台区天气：\n{desc_match.group(1)}"
    else:
        # 备用方案：从页面提取
        temp_match = re.search(r'<div class="wea_weather">\s*<em>(.*?)</em>', html)
        weather_match = re.search(r'<div class="wea_weather">\s*<b>(.*?)</b>', html)
        temp_range_match = re.search(r'<div class="wea_weather">\s*<span>(.*?)</span>', html)
        
        weather_info = "南京雨花台区天气：\n"
        if temp_match:
            weather_info += f"温度: {temp_match.group(1)}℃\n"
        if weather_match:
            weather_info += f"天气: {weather_match.group(1)}\n"
        if temp_range_match:
            weather_info += f"气温范围: {temp_range_match.group(1)}"
    
    print(f"获取到的天气: {weather_info}")
    send_wechat_msg(weather_info)

except Exception as e:
    error_msg = f"获取天气失败: {e}"
    print(error_msg)
    send_wechat_msg(error_msg)
