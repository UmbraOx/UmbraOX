"""
conftest.py — place this in C:\Umbra\ (root, same folder as umbra.py)
Fixes: ModuleNotFoundError: No module named 'umbra' in test_umbra_entry.py
"""
import sys
import os

# Ensure C:\Umbra is on sys.path so pytest can import umbra.py directly
_root = os.path.dirname(os.path.abspath(__file__))
if _root not in sys.path:
    sys.path.insert(0, _root)