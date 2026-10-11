# Win7 Kimi API 部署方案

> 在一台 2013 年的 Windows 7 台式机上跑通 Kimi 的 OpenAI 兼容 API，并通过 Cloudflare Tunnel 暴露到公网。

## 为什么需要这个方案

Windows 7 无法运行 Node 14+ 的原生模块（`esbuild`、`rollup` 等），也无法运行 Electron 23+（Chat2API 等现代客户端）。本仓库记录了在 Win7 上部署 Kimi API 的完整踩坑过程。

## 最终效果

- 本地：`http://localhost:8000/v1/chat/completions` 返回 200
- 公网：`https://api.your-domain.com/v1/chat/completions` 返回 200
- 开机自启、无窗口、token 自动刷新
- 全程零成本（不含 VPN）

## 技术栈

| 组件 | 版本 | 作用 |
|---|---|---|
| Python | 3.11.16 | 辅助脚本 |
| Node.js | 18.20.0（真版） | 运行 Kimi-Free-API |
| Kimi-Free-API | 1.0.2 | 提供 OpenAI 兼容接口 |
| cloudflared | 2026.10.0（打过补丁） | 内网穿透 |

## 关键补丁

### 补丁 1：绕过 `uv_os_gethostname` 的 ENOSYS 错误

**现象**：`formidable` 包加载时抛 `SystemError: uv_os_gethostname returned ENOSYS`。

**原因**：Win7 的 `ws2_32.dll` 缺少 `GetHostNameW` 函数，Node.js 的 libuv 层直接报错。

**解法**：`patch.js`

```js
const os = require('os');
os.hostname = function () { return 'localhost'; };
```

启动时通过 `--require ./patch.js` 注入。

### 补丁 2：跳过 esbuild 原生编译

**现象**：`npm install` 时 esbuild postinstall 报 `Exception 0xc0000005`。

**解法**：`npm install --ignore-scripts`。所有依赖都是纯 JS，跳过脚本不影响运行。

同时需要把 `mime` 从 v4 降到 v3.0.0（v4+ 是纯 ESM 模块，CommonJS 无法 `require`）。

### 补丁 3：cloudflared 在 Win7 上的崩溃修复

**现象**：新版 cloudflared 报 `Exception 0xc0000005`，无法启动。

**原因**：新 Go 编译器生成的代码调用了 Win8+ 才有的 API。

**解法**：用 [golangwin7patch](https://github.com/stunndard/golangwin7patch) 的 `GoWin7Fixer.exe` 打补丁。

## 部署步骤

### 1. 准备真 Node 18

如果你机器上的 `node.exe` 是某个魔改版（`node --version` 显示 v26 但目录名是 v18），把官方 Node 18 的二进制重命名为 `node.exe.bak`，避免冲突。

验证：

```cmd
node.exe.bak --version
:: 应输出 v18.20.0
```

### 2. 安装 Kimi-Free-API

```cmd
git clone https://github.com/xiaoY233/Kimi-Free-API.git
cd Kimi-Free-API
npm install --ignore-scripts
npm install mime@3.0.0 --ignore-scripts
```

### 3. 建补丁文件

在项目根目录创建 `patch.js`（内容见上）。

### 4. 启动服务

```cmd
"<真Node路径>\node.exe.bak" --require ./patch.js dist/index.js
```

看到 `Server listening on port 8000` 即成功。

### 5. 无窗口 + 开机自启

`run.bat`：

```bat
@echo off
cd /d <项目路径>
"<真Node路径>\node.exe.bak" --require ./patch.js dist/index.js > run.log 2>&1
```

`start-kimi-free.vbs`：

```vbs
Set WShell = CreateObject("WScript.Shell")
WShell.Run """<项目路径>\run.bat""", 0, False
```

把 VBS 的快捷方式丢进 `shell:startup`。

### 6. Cloudflare Tunnel

```cmd
cloudflared tunnel login
cloudflared tunnel create kimi-tunnel
cloudflared tunnel route dns kimi-tunnel api.your-domain.com
cloudflared tunnel --protocol http2 run kimi-tunnel
```

配置 `~/.cloudflared/config.yml`：

```yaml
tunnel: kimi-tunnel
credentials-file: C:\Users\<你>\.cloudflared\<UUID>.json

ingress:
  - hostname: api.your-domain.com
    service: http://127.0.0.1:8000
  - service: http_status:404
```

## 踩坑记录

详见 [docs/troubleshooting.md](docs/troubleshooting.md)。

## 安全提醒

- **不要暴露 refresh_token**（任何人拿到都能用你的 Kimi 额度）
- 建议开启 Cloudflare Access（邮箱验证）作为第二层防护
- 逆向 API 存在账号封禁风险，仅用于个人研究

## License

MIT