# Win31 Agent

A Windows 3.1 **styled** AI research agent.

Real Win 3.1 (1992, 16-bit) cannot run Python. But the visual style? Absolutely.

## What it looks like

    +------------------------------------------------------------------+
    | Program Manager - [WIN31AGENT.EXE]                               |
    +------------------------------------------------------------------+
    |  File    Edit    View    Options    Help                         |
    +------------------------------------------------------------------+
    |                                                                  |
    |   WIN31AGENT  AI Research Agent                                  |
    |   Copyright (C) 1992-2026                                        |
    |                                                                  |
    +------------------------------------------------------------------+

    C:\WIN31> AGENT.EXE "solid state battery"
    [1/3] searching...
    [2/3] generating report...
    [3/3] done

## Why

Nostalgia. Also, Win 3.1 is a 16-bit OS from 1992 that cannot run Python 3 at all. So we made a Python 3 agent that *looks* like Win 3.1.

## Features

- Blue background (ANSI color 17)
- ASCII box windows
- C:\WIN31> DOS prompt
- Program Manager title bar
- File/Edit/View/Options/Help menu bar
- Real Bing search + LLM

## Usage

    set BACKEND=zhipu
    set OPENAI_API_KEY=sk-xxx
    python win31_agent.py "solid state battery"

## Series

- v0.1: open-research-agent (Win7, 500 lines)
- v0.2: xp-agent (XP, 29 lines)
- v0.3: win2000-agent (Win2000, Py2.7)
- v0.4: win31-agent (this repo, Win 3.1 style)

## License

MIT
