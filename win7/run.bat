@echo off
cd /d D:\ZhouYongJie\kimi-proj\Kimi-Free-API
"D:\ZhouYongJie\Download\node-v18.20.0-win-x64\node.exe.bak" --require ./patch.js dist\index.js > run.log 2>&1