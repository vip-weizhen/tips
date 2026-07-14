#! -*- coding: utf-8 -*-
"""
Author: Mr.wei
Update: 2026-07-14
Info: 每日工作报备温馨提醒
cron: 30 17 * * *
new Env('工作报备');
"""
import requests
import json
from datetime import datetime, timedelta

wx_url = ""

def send_msg(content, mention_all=False):
    """发送企业微信消息"""
    data = {
        "msgtype": "text",
        "text": {
            "content": content
        }
    }
    if mention_all:
        data["text"]["mentioned_list"] = ["@all"]
    
    try:
        response = requests.post(wx_url, json=data, timeout=10)
        if response.status_code == 200:
            print(f"消息发送成功: {content[:30]}...")
        else:
            print(f"消息发送失败: {response.status_code}")
        return response.json()
    except Exception as e:
        print(f"发送异常: {e}")
        return None

def get_weekday():
    """获取星期几"""
    weekdays = ['一', '二', '三', '四', '五', '六', '日']
    return weekdays[datetime.now().weekday()]

def generate_warm_message():
    """生成温馨提醒文案"""
    today = datetime.now().strftime('%m月%d日')
    weekday = get_weekday()
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%m月%d日')
    
    messages = [
        f"🌅 各位同事下午好！\n\n"
        f"今天是{today} 星期{weekday}，\n"
        f"温馨提醒：为了明天的工作更高效，\n"
        f"请大家在18:00前将【{tomorrow}的工作计划】\n"
        f"发到群里，谢谢配合！🙏",
        
        f"⏰ 温馨提示\n\n"
        f"计划还没发的同事别着急，\n"
        f"还有30分钟截止哦~\n"
        f"记得把明天{ tomorrow}的计划发一下~ 📝",
        
        f"☕️ 最后提醒\n\n"
        f"距离截止还有最后10分钟！\n"
        f"请大家抓紧时间提交明日计划，\n"
        f"让我们一起把工作做得更好！💪"
    ]
    
    return messages

def main():
    """主函数"""
    print(f"开始发送工作报备提醒... {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 生成温馨提醒文案
    messages = generate_warm_message()
    
    # 第一轮：主要提醒（@所有人）
    print("发送第一轮提醒...")
    send_msg(messages[0], mention_all=True)
    
    # 等待30分钟后发送第二次提醒
    print("等待30分钟后发送第二轮提醒...")
    time.sleep(1800)  # 30分钟
    
    # 第二轮：温和提醒
    print("发送第二轮提醒...")
    send_msg(messages[1], mention_all=False)
    
    # 等待20分钟后发送最后提醒
    print("等待20分钟后发送最后一轮提醒...")
    time.sleep(1200)  # 20分钟
    
    # 第三轮：最后提醒
    print("发送最后一轮提醒...")
    send_msg(messages[2], mention_all=False)
    
    print("所有提醒发送完成！")

if __name__ == "__main__":
    main()
