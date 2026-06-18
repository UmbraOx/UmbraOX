@echo off
title UMBRA -- Autonomous AI Runtime OS v2.0.0
cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo [UMBRA] Virtual environment not found. Creating...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install pytest pytest-timeout
) else (
    call venv\Scripts\activate.bat
)

if not exist "umbra_config.json" (
    echo [UMBRA] First run detected. Running setup wizard...
    python umbra_setup.py
)

python umbra.py %*
pause