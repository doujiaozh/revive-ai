import os, sys, json, re, urllib.request, urllib.parse
KEY = os.environ.get("OPENAI_API_KEY")
URL = os.environ.get("OPENAI_BASE_URL", "").rstrip("/")
MODEL = os.environ.get("MODEL", "gpt-4o-mini")
def post(path, body):
    req = urllib.request.Request(URL+path, data=json.dumps(body).encode(),
        headers={"Content-Type":"application/json","Authorization":"Bearer "+KEY})
    return json.loads(urllib.request.urlopen(req, timeout=180).read())
def search(q):
    req = urllib.request.Request("https://cn.bing.com/search?q="+urllib.parse.quote(q),
        headers={"User-Agent":"Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8","ignore")
    out = []
    for c in re.split(r'<li class="b_algo"', html)[1:6]:
        m = re.search(r'<h2[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', c, re.S)
        if m: out.append(re.sub(r"<[^>]+>","",m.group(2)) + "\n" + m.group(1))
    return "\n".join(out)
def main(g):
    print("[XP] 目标:", g)
    print("[XP] 搜索中...")
    s = search(g)
    print(s[:300])
    print("[XP] 生成报告...")
    r = post("/chat/completions", {"model":MODEL,
        "messages":[{"role":"user","content":"基于以下资料写 Markdown 研究报告《"+g+"》，末尾列出来源 URL。\n\n"+s}],
        "max_tokens":2048})
    print("="*50)
    print(r["choices"][0]["message"].get("content") or "")
main(sys.argv[1] if len(sys.argv) > 1 else "固态电池")
