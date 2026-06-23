import requests
import re
from datetime import datetime
import time

# ========================
# Cloudflare API 参数 (Token 对所有 Zone 有效即可)
# ========================
api_token = ""

# 企业微信机器人
WXWORK_WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key="

# ========================
# 核心配置：顶级域名  ->  Zone ID
# 请务必用你真实的 Zone ID 替换下面的占位符
# ========================
ZONE_MAPPING = {
    ".cloudns.org": "",
    ".cloudns.org":  ""
}

# ========================
# 地区 → 域名映射
# 格式：(子域名前缀, 顶级域名)
# ========================
REGION_DOMAIN_MAP = {
    "HK": ("yxhk", ".cloudns.org"),
    "US": ("yxus", ".cloudns.org"),
    "SG": ("yxsg", ".cloudns.org"),
    "JP": ("yxjp", ".cloudns.org")
}

MAX_IPS_PER_REGION = 10


# ========================
# 工具函数
# ========================
def send_wxwork(content):
    try:
        payload = {"msgtype": "markdown", "markdown": {"content": content}}
        r = requests.post(WXWORK_WEBHOOK, json=payload, timeout=10)
        data = r.json()
        if r.status_code == 200 and data.get("errcode") == 0:
            print("📨 企业微信通知发送成功")
        else:
            print("⚠️ 企业微信通知失败：", data)
    except Exception as e:
        print("⚠️ 企业微信异常：", e)

def get_zone_config(domain):
    for zone_domain, zone_id in ZONE_MAPPING.items():
        if domain.endswith(zone_domain):
            return {
                "api_base": f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
                "headers": {
                    "Authorization": f"Bearer {api_token}",
                    "Content-Type": "application/json"
                }
            }
    return None

# ========================
# 带重试机制的 API 请求
# ========================
def request_with_retry(method, url, headers, **kwargs):
    max_retries = 3
    for attempt in range(max_retries):
        try:
            if method == 'GET':
                return requests.get(url, headers=headers, timeout=20, **kwargs)
            elif method == 'POST':
                return requests.post(url, headers=headers, timeout=20, **kwargs)
            elif method == 'DELETE':
                return requests.delete(url, headers=headers, timeout=20, **kwargs)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            if attempt < max_retries - 1:
                print(f"⚠️ 网络连接异常，{attempt + 1}秒后重试... (错误: {e})")
                time.sleep(attempt + 1)
            else:
                raise e
    return None

# ========================
# 智能同步函数（核心修改）
# ========================
def sync_dns_records(subdomain, target_ips):
    zone_conf = get_zone_config(subdomain)
    if not zone_conf:
        print(f"❌ 找不到 {subdomain} 对应的 Zone ID")
        return [], []

    api_base = zone_conf["api_base"]
    headers = zone_conf["headers"]

    try:
        # 1. 获取当前 Cloudflare 上所有的 A 记录
        find_resp = request_with_retry('GET', api_base, headers, params={"name": subdomain, "type": "A"})
        existing_records = find_resp.json().get("result", [])
        
        current_ips = {rec['content']: rec['id'] for rec in existing_records}
        target_set = set(target_ips)

        # 2. 计算需要删除的 IP (当前存在，但新列表里没有的)
        ips_to_delete = current_ips.keys() - target_set
        
        # 3. 计算需要新增的 IP (新列表有，但当前不存在的)
        ips_to_add = target_set - current_ips.keys()

        print(f"  现状: {len(current_ips)} 条记录 | 需要删除: {len(ips_to_delete)} 条 | 需要新增: {len(ips_to_add)} 条")

        # 4. 执行删除
        deleted_ips = []
        for ip in ips_to_delete:
            record_id = current_ips[ip]
            try:
                request_with_retry('DELETE', f"{api_base}/{record_id}", headers)
                deleted_ips.append(ip)
                print(f"  🗑️ 清理废弃记录: {ip}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  ❌ 删除 {ip} 失败: {e}")

        # 5. 执行新增
        added_ips = []
        for ip in ips_to_add:
            try:
                payload = {"type": "A", "name": subdomain, "content": ip, "ttl": 1, "proxied": False}
                request_with_retry('POST', api_base, headers, json=payload)
                added_ips.append(ip)
                print(f"  ➕ 新增记录: {ip}")
                time.sleep(0.5)
            except Exception as e:
                print(f"  ❌ 添加 {ip} 失败: {e}")

        # 返回结果：成功列表 = 原本就有的 + 新添加成功的
        success_ips = list(target_set - set(ips_to_delete) - (set(ips_to_add) - set(added_ips)))
        failed_ips = list(set(ips_to_add) - set(added_ips))
        
        return success_ips, failed_ips

    except Exception as e:
        print(f"❌ 同步操作异常: {e}")
        return [], target_ips


# ========================
# 主程序
# ========================
print("=" * 60)
print("📡 正在拉取优选IP数据...")

url = "https://raw.githubusercontent.com/svip-s/cloudflare_ip/refs/heads/main/best_ips.txt"

try:
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"HTTP {resp.status_code}")
except Exception as e:
    msg = f"## ❌ 拉取数据失败\n> {e}\n> 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    send_wxwork(msg)
    raise SystemExit

# 解析 IP
region_ips = {region: [] for region in REGION_DOMAIN_MAP}
for line in resp.text.splitlines():
    line = line.strip()
    if not line: continue
    match = re.match(r'^(\d{1,3}(?:\.\d{1,3}){3}):\d+#([A-Z]{2,3})', line)
    if match:
        ip, region = match.group(1), match.group(2)
        if region in region_ips:
            region_ips[region].append(ip)

# 去重、限流
for region in region_ips:
    region_ips[region] = list(dict.fromkeys(region_ips[region]))[:MAX_IPS_PER_REGION]
    print(f"📍 {region} 获取到 {len(region_ips[region])} 个 IP")

notify_lines = [
    f"## 🌐 Cloudflare优选IP更新报告",
    f"> 时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    ""
]

total_success = 0
total_fail = 0

# 主循环
for region, (sub_prefix, zone_domain) in REGION_DOMAIN_MAP.items():
    full_domain = f"{sub_prefix}.{zone_domain}"
    ips = region_ips.get(region, [])
    
    print("\n" + "=" * 60)
    print(f"处理 {region} → {full_domain}")

    notify_lines.append(f"### {region}")
    notify_lines.append(f"> 域名：`{full_domain}`")

    if not ips:
        print("⚠️ 未获取到IP，跳过")
        notify_lines.append("> ⚠️ 未获取到IP")
        notify_lines.append("")
        continue

    # 核心同步逻辑（集成了查询、对比、删除、新增、重试）
    success_ips, fail_ips = sync_dns_records(full_domain, ips)

    total_success += len(success_ips)
    total_fail += len(fail_ips)

    notify_lines.append(f"> ✅ 有效/新增 {len(success_ips)} 条")
    notify_lines.append(f"> ❌ 失败 {len(fail_ips)} 条")
    if success_ips:
        notify_lines.extend([f"> `{ip}`" for ip in success_ips])
    if fail_ips:
        notify_lines.append(f"> 失败IP：{', '.join(fail_ips)}")
    notify_lines.append("")

notify_lines.append("---")
notify_lines.append(f"📊 汇总：成功 {total_success} 条，失败 {total_fail} 条")

print("\n📨 发送企业微信通知...")
send_wxwork("\n".join(notify_lines))

print("\n🎉 更新完成")
