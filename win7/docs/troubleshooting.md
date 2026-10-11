踩坑记录
坑 1：Node 版本迷惑
现象：目录名是 node-v18.20.0-win-x64，但 node --version 显示 v26.7.0。

原因：node.exe 被替换成了魔改版，官方 Node 18 被备份成 node.exe.bak。

解法：直接用 node.exe.bak 全路径调用。

坑 2：npm install 卡在 idealTree buildDeps
原因：electron 二进制从 GitHub 下载超时。

解法：设镜像。

text
set ELECTRON_MIRROR=https://npmmirror.com/mirrors/electron/
set ELECTRON_BUILDER_BINARIES_MIRROR=https://npmmirror.com/mirrors/electron-builder-binaries/
坑 3：package.json 的 BOM 问题
现象：electron-builder 报 expect { or n, but found 奇怪字符。

原因：记事本保存 UTF-8 时自动加 BOM，Go 写的解析器不认。

解法：用 Node 去 BOM。

text
node -e "const fs=require('fs');const p='package.json';let s=fs.readFileSync(p,'utf8');if(s.charCodeAt(0)===0xFEFF){s=s.slice(1);fs.writeFileSync(p,s,'utf8');}"
坑 4：Cloudflare Tunnel 530 错误
现象：https://api.your-domain.com 返回 530。

原因：DNS 记录指向的 Tunnel UUID 和实际运行的 Tunnel 不一致。

解法：删掉旧 DNS 记录，重新 cloudflared tunnel route dns <tunnel-name> <hostname>。

坑 5：Electron 降级失败
尝试：把 Chat2API 的 Electron 从 33 降到 22.3.27（Win7 最后支持版本）。

结果：能打包、能启动界面，但 API 请求全部返回 500，异常被吞掉。

结论：降级 Electron 无法解决所有依赖问题。Chat2API 在 Win7 上不可用，放弃。