# -*- coding: gbk -*-
import os, sys, json, re
import urllib.request, urllib.parse

W = 68

def clear():
    os.system('cls')

def box_top(title):
    print("+" + "-" * (W - 2) + "+")
    print("| " + title.ljust(W - 4) + " |")
    print("+" + "-" * (W - 2) + "+")

def box_menu():
    m = " File    Edit    View    Options    Help"
    print("| " + m.ljust(W - 4) + " |")
    print("+" + "-" * (W - 2) + "+")

def box_text(text):
    print("| " + text.ljust(W - 4) + " |")

def box_bottom():
    print("+" + "-" * (W - 2) + "+")

BACKENDS = {
    "zhipu":       ("https://open.bigmodel.cn/api/paas/v4", "glm-4-flash"),
    "deepseek":    ("https://api.deepseek.com/v1",          "deepseek-chat"),
    "siliconflow": ("https://api.siliconflow.cn/v1",        "Qwen/Qwen2.5-7B-Instruct"),
}
BACKEND = os.environ.get("BACKEND", "zhipu")
KEY     = os.environ.get("OPENAI_API_KEY", "")
default_url, default_model = BACKENDS.get(BACKEND, ("", ""))
URL   = os.environ.get("OPENAI_BASE_URL", default_url).rstrip("/")
MODEL = os.environ.get("MODEL", default_model)

def post(path, body):
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(URL + path, data=data,
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + KEY})
    raw = urllib.request.urlopen(req, timeout=180).read()
    return json.loads(raw.decode("utf-8"))

def get(url):
    req = urllib.request.Request(url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 3.1)",
                 "Accept-Language": "zh-CN,zh;q=0.9"})
    raw = urllib.request.urlopen(req, timeout=30).read()
    return raw.decode("utf-8", "ignore")

def search(q):
    try:
        html = get("https://cn.bing.com/search?q=" + urllib.parse.quote(q) + "&mkt=zh-CN")
        out = []
        for c in re.split(r'<li class="b_algo"', html)[1:6]:
            m = re.search(r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', c, re.S)
            if m:
                t = re.sub(r"<[^>]+>", "", m.group(2)).strip()
                out.append("- " + t + "\n  " + m.group(1))
        return "\n".join(out)
    except Exception as e:
        return "搜索失败: " + str(e)

def main(goal):
    clear()
    os.system("color 17")
    box_top("Program Manager - [WIN31AGENT.EXE]")
    box_menu()
    box_text("")
    box_text("  WIN31AGENT  AI Research Agent")
    box_text("  Copyright (C) 1992-2026")
    box_text("")
    box_bottom()

    print()
    print("C:\\WIN31> AGENT.EXE \"" + goal + "\"")
    print()

    print("[1/3] 搜索中...")
    s = search(goal)
    print("      获取 " + str(len(s)) + " 字符")

    print("[2/3] 生成报告中...")
    prompt = ("用中文写一份关于《" + goal + "》的 Markdown 研究报告。"
              "严格要求：1. 只基于下面资料，不要编造。"
              "2. 末尾列出资料中出现的 URL。3. 用中文输出。\n\n资料：\n" + s)
    r = post("/chat/completions", {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2048
    })
    report = r["choices"][0]["message"].get("content", "")

    print("[3/3] 完成")
    print()
    box_top("Message")
    print(report)
    box_bottom()
    print()
    print("C:\\WIN31> _")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python win31_agent.py \"研究主题\"")
        sys.exit(1)
    main(sys.argv[1])