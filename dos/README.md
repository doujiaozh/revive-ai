# DOS 6.22 / FreeDOS AI Agent

在 1981 年的 DOS 系统上，通过 QEMU 模拟器与 mTCP 协议栈，成功连接现代 Kimi API。

## 架构
DOS (FreeDOS 1.4)
└── NE2000 网卡驱动 (Crynwr)
└── mTCP 协议栈 (TCP/IP)
└── HTTP 请求
↓
QEMU Slirp 虚拟网关 (10.0.2.2)
↓
Windows Python 代理 (localhost:8080)
↓
Kimi-Free-API (localhost:8000)
↓
Kimi 官方 API (HTTPS)

## 成果证明

- DOS 里 `HTGET.EXE` 成功返回 `200 OK`。
- 代理日志显示 `[KIMI<-] 200`，成功接收并处理大模型回复。
- 适配了 `doschgpt` 客户端，因客户端自身解析旧 JSON 格式存在 Bug，暂演示 HTTP 底层链路。

## 部署说明

详见 `win7/docs/troubleshooting.md` 中的网络配置与 QEMU 踩坑记录。