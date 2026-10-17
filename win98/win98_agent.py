# -*- coding: utf-8 -*-

# win98_agent.py - Win 98 styled AI research agent

# Python 2.7 / 3.x compatible

import os, sys, json, re

PY3 = sys.version_info[0] >= 3

if PY3:

    from urllib.request import Request, urlopen

    from urllib.parse import quote

else:

    from urllib2 import Request, urlopen

    from urllib import quote



W = 72

BACKENDS = {

    "zhipu":       ("https://open.bigmodel.cn/api/paas/v4", "glm-4-flash"),

    "deepseek":    ("https://api.deepseek.com/v1",          "deepseek-chat"),

    "siliconflow": ("https://api.siliconflow.cn/v1",        "Qwen/Qwen2.5-7B-Instruct"),

}

BACKEND = os.environ.get("BACKEND", "zhipu")

KEY     = os.environ.get("OPENAI_API_KEY", "")

durl, dmodel = BACKENDS.get(BACKEND, ("", ""))

URL   = os.environ.get("OPENAI_BASE_URL", durl).rstrip("/")

MODEL = os.environ.get("MODEL", dmodel)



def line():

    print("+" + "-" * (W - 2) + "+")



def title(t):

    line()

    print("| " + t.ljust(W - 4) + " |")

    line()



def menu():

    print("| File   Edit   View   Go   Favorites   Help".ljust(W - 1) + "|")

    line()



def box_open(t):

    line()

    print("| " + t.ljust(W - 4) + " |")

    line()



def box_close():

    line()



def post(path, body):

    data = json.dumps(body).encode("utf-8")

    req = Request(URL + path, data=data)

    req.add_header("Content-Type", "application/json")

    req.add_header("Authorization", "Bearer " + KEY)

    raw = urlopen(req, timeout=180).read()

    if isinstance(raw, bytes):

        raw = raw.decode("utf-8")

    return json.loads(raw)



def get(url):

    req = Request(url)

    req.add_header("User-Agent", "Mozilla/5.0 (Windows 98; Win 9x 4.90)")

    req.add_header("Accept-Language", "zh-CN,zh;q=0.9")

    raw = urlopen(req, timeout=30).read()

    if isinstance(raw, bytes):

        raw = raw.decode("utf-8", "ignore")

    return raw



def search(q):

    try:

        url = "https://cn.bing.com/search?q=" + quote(q) + "&mkt=zh-CN"

        html = get(url)

        out = []

        for c in re.split(r'<li class="b_algo"', html)[1:6]:

            m = re.search(r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', c, re.S)

            if m:

                t = re.sub(r"<[^>]+>", "", m.group(2)).strip()

                out.append("- " + t + "\n  " + m.group(1))

        return "\n".join(out)

    except Exception as e:

        return "search failed: " + str(e)



def main(goal):

    os.system("cls" if os.name == "nt" else "clear")

    if os.name == "nt":

        os.system("color 07")

    title("Win98 Agent - C:\\MYDOCU~1\\AGENT.EXE")

    menu()

    print("| " + "".ljust(W - 4) + " |")

    print("| " + "  Microsoft Windows 98".ljust(W - 4) + " |")

    print("| " + "  AI Research Agent".ljust(W - 4) + " |")

    print("| " + "  Copyright (C) 1998-2026".ljust(W - 4) + " |")

    print("| " + "".ljust(W - 4) + " |")

    box_close()

    print("")

    print("C:\\WINDOWS\\Desktop> AGENT.EXE \"" + goal + "\"")

    print("")

    print("[1/3] Searching the web...")

    s = search(goal)

    print("      got " + str(len(s)) + " chars")

    print("[2/3] Generating report...")

    prompt = ("用中文写一份关于《" + goal + "》的 Markdown 研究报告。"

              "严格要求：1. 只基于下面资料，不要编造。"

              "2. 末尾列出资料中出现的 URL。3. 用中文输出。\n\n资料：\n" + s)

    r = post("/chat/completions", {

        "model": MODEL,

        "messages": [{"role": "user", "content": prompt}],

        "max_tokens": 2048

    })

    report = r["choices"][0]["message"].get("content", "")

    print("[3/3] Done.")

    print("")

    box_open("Message")

    print(report)

    box_close()

    print("")

    print("C:\\WINDOWS\\Desktop> _")



if __name__ == "__main__":

    if len(sys.argv) < 2:

        print("Usage: python win98_agent.py \"topic\"")

        sys.exit(1)

    main(sys.argv[1])

