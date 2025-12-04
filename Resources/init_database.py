#!/usr/bin/env python3
"""Initialize Perfect Memory Database"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from memory_core import initialize_database

result = initialize_database()
print(f"Database initialized: {result['database']}")
print(f"Status: {result['status']}")