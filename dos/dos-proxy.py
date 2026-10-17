from http.server import BaseHTTPRequestHandler, HTTPServer
import httpx, json, urllib.parse

API = "http://localhost:8000"
TOKEN = "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhY2NvdW50IiwiYXVkIjpbImtpbWkuY29tIl0sImV4cCI6MTc5OTE0NTAzNiwiaWF0IjoxNzkxMzY5MDM2LCJqdGkiOiJkYjMxdWowN2RsYzM2MTNlbHFhZyIsInR5cCI6InJlZnJlc2giLCJhcHBfaWQiOiJraW1pIiwic3ViIjoiZDk4cGZib2c5NWdpMGtxbGduamciLCJhYnN0cmFjdF91c2VyX2lkIjoiZDk4cGZib2c5NWdpMGtxbGduaWciLCJzc2lkIjoiMTczMTc1MDYwNTAzMjExMzc0NSIsImRldmljZV9pZCI6Ijc1NjIxNjkzOTY0NzEzMTU5ODAiLCJyZWdpb24iOiJjbiIsIm1lbWJlcnNoaXAiOnsibGV2ZWwiOjEwfSwiY29kZV9tZW1iZXJzaGlwIjp7ImxldmVsIjoxMH19.6tNraRvt8gYVm5YVL3ve9fcJMwB7JZoeWXAMzAQBiNmnoAmdcDWYOEf0wERUvx7KLzN3EtEooehzV2BfvPqwgQ"

class P(BaseHTTPRequestHandler):
    def do_GET(self):
        if not self.path.startswith("/ask"):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            return
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get("q",[""])[0]
        body = json.dumps({"model":"kimi-k2-0905-preview","messages":[{"role":"user","content":q}],"temperature":0.7,"stream":False}).encode("utf-8")
        try:
            with httpx.Client(timeout=180) as c:
                r = c.post(API + "/v1/chat/completions", content=body, headers={"Authorization":"Bearer "+TOKEN,"Content-Type":"application/json"})
                text = r.json()["choices"][0]["message"]["content"]
                clean = "".join([c for c in text if 32 <= ord(c) <= 126])
                out = clean.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(out)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())
    def log_message(self, *a): pass

print("proxy running 8080...", flush=True)
HTTPServer(("0.0.0.0", 8080), P).serve_forever()