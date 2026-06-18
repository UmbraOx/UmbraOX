@echo off
cd /d C:\Umbra

echo Starting Umbra Runtime System...

call venv\Scripts\activate

python run_umbra.py

pause