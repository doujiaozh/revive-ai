# XP Agent

An AI research agent that runs on **Windows XP + Python 3.4**.

**Pure stdlib. Zero dependencies. ~30 lines.**

## What it does

Give it a topic. It searches Bing, calls an OpenAI-compatible LLM, prints a Markdown report.

## Why pure stdlib

Windows XP caps Python at 3.4.4. Modern AI stacks (httpx, pydantic 2.x, openai SDK) all need Rust binaries that XP cannot load. So this agent uses only:
- urllib.request
- json
- re
- ssl

## Quick start

    export OPENAI_API_KEY=sk-xxx
    export OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
    export MODEL=glm-4-flash
    python xp_agent.py "solid state battery"

## Recommended backends

- Zhipu GLM-4-Flash (free tier): https://open.bigmodel.cn
- SiliconFlow: https://api.siliconflow.cn/v1
- DeepSeek: https://api.deepseek.com/v1

## Verified on

- Termux (Android, Python 3.14) - working
- Windows XP + Python 3.4.4 - code compatible (not yet tested on real XP)

## License

MIT
