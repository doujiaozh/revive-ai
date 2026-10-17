# Win98 Agent

A Windows 98 **styled** AI research agent.

Real Win98 can run Python 2.7 (with some fiddling). This agent uses the same loop as the other legacy agents, but looks like 1998.

## What it looks like

    +----------------------------------------------------------------------+
    | Win98 Agent - C:\MYDOCU~1\AGENT.EXE                                  |
    +----------------------------------------------------------------------+
    | File   Edit   View   Go   Favorites   Help                           |
    +----------------------------------------------------------------------+
    |                                                                      |
    |   Microsoft Windows 98                                               |
    |   AI Research Agent                                                  |
    |   Copyright (C) 1998-2026                                            |
    |                                                                      |
    +----------------------------------------------------------------------+

    C:\WINDOWS\Desktop> AGENT.EXE "solid state battery"
    [1/3] Searching the web...
    [2/3] Generating report...
    [3/3] Done.

## Why

1998 nostalgia. Also, `C:\WINDOWS\Desktop>` is the most iconic DOS prompt in history.

## Features

- Win98-style ASCII box windows
- File/Edit/View/Go/Favorites/Help menu bar
- C:\WINDOWS\Desktop> prompt
- Multi-backend LLM support (Zhipu / DeepSeek / SiliconFlow)
- Real Bing search

## Usage

    set BACKEND=zhipu
    set OPENAI_API_KEY=sk-xxx
    python win98_agent.py "solid state battery"

## Series

- v0.1: [open-research-agent](https://github.com/doujiaozh/open-research-agent) (Win7, 500 lines)
- v0.2: [xp-agent](https://github.com/doujiaozh/xp-agent) (XP, 29 lines)
- v0.3: [win2000-agent](https://github.com/doujiaozh/win2000-agent) (Win2000, Py2.7)
- v0.4: [win31-agent](https://github.com/doujiaozh/win31-agent) (Win 3.1, visual style)
- v0.5: **win98-agent (this repo, Win98 style)**

## License

MIT
