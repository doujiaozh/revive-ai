import urllib.request, json, ssl

URL = "https://api.doujiao.ccwu.cc/v1/chat/completions"
TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhY2NvdW50IiwiYXVkIjpbImtpbWkuY29tIl0sImV4cCI6MTc5OTE0NTAzNiwiaWF0IjoxNzkxMzY5MDM2LCJqdGkiOiJkYjMxdWowN2RsYzM2MTNlbHFhZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiZDk4cGZib2c5NWdpMGtxbGduamciLCJhYnN0cmFjdF91c2VyX2lkIjoiZDk4cGZib2c5NWdpMGtxbGduaWciLCJzc2lkIjoiMTczMTc1MDYwNTAzMjExMzc0NSIsImRldmljZV9pZCI6Ijc1NjIxNjkzOTY0NzEzMTU5ODAiLCJyZWdpb24iOiJjbiIsIm1lbWJlcnNoaXAiOnsibGV2ZWwiOjEwfSwiY29kZV9tZW1iZXJzaGlwIjp7ImxldmVsIjoxMH19.6tNraRvt8gYVm5YVL3ve9fcJMwB7JZoeWXAMzAQBiNmnoAmdcDWYOEf0wERUvx7KLzN3EtEooehzV2BfvPqwgQ"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

print("====================================")
print(" Revive-AI 手机终端极简版 (Zero-Dep)")
print(" 输入 exit 退出")
print("====================================")

while True:
    try:
        q = input("\nYou: ")
        if q.lower() in ["exit", "quit"]: break
        data = json.dumps({"model": "kimi-k2-0905-preview", "messages": [{"role": "user", "content": q}]}).encode("utf-8")
        req = urllib.request.Request(URL, data=data, headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}, method="POST")
        print("Thinking...", end="", flush=True)
        with urllib.request.urlopen(req, context=ctx, timeout=60) as r:
            res = json.loads(r.read().decode("utf-8"))
            print("\rAI:", res["choices"][0]["message"]["content"])
    except Exception as e:
        print("\r[Error] 请求失败，请检查电脑是否开机。")
