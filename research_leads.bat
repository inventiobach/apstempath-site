@echo off
chcp 65001 > nul
title X Lead Finder - AP STEM PATH

echo ========================================================
echo   X (Twitter) 見込み客リサーチ・ダッシュボードを起動中...
echo   AP STEM PATH | 1日2分ルーティン
echo ========================================================
echo.

python "%~dp0scripts\x_lead_finder.py"

pause
