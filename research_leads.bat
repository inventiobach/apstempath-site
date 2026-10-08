@echo off
title X Lead Finder - AP STEM PATH

if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" "%~dp0scripts\x_lead_finder.py"
) else (
    python "%~dp0scripts\x_lead_finder.py"
)

pause
