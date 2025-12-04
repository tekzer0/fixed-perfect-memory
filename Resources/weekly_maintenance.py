#!/usr/bin/env python3
"""Run weekly maintenance and curation."""

import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from memory_core import weekly_maintenance

if __name__ == "__main__":
    print("🧹 Running weekly maintenance...")
    result = weekly_maintenance()
    print(json.dumps(result, indent=2))
