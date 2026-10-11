Set WShell = CreateObject("WScript.Shell")
WShell.Run """D:\ZhouYongJie\Download\cloudflared-windows-amd64.exe"" tunnel --protocol http2 run kimi-tunnel", 0, False