@echo off
title UMBRA
cd /d "%~dp0"
call venv\Scripts\activate.bat
python umbra.py %*