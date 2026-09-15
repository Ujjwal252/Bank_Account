"""
run.py — Project root runner for the Bank Account demo.

Usage (from project root):
    python run.py
"""

import sys
import os

# Add project root to path so 'src' is importable
sys.path.insert(0, os.path.dirname(__file__))

from src.main import main

if __name__ == "__main__":
    main()
