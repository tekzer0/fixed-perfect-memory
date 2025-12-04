#!/usr/bin/env python3
"""Store a discovered ability in persistent memory."""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/mnt/s/claude-perfect-memory/database/memory.db")

def store_ability(ability: str, description: str):
    """Store an ability."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    key = f"ability_{ability.lower().replace(' ', '_').replace('-', '_')}"
    value = json.dumps({
        "ability": ability,
        "description": description,
        "discovered_at": datetime.now().isoformat()
    })
    
    c.execute('''INSERT OR REPLACE INTO short_term_memory (key, value, category, updated_at)
                 VALUES (?, ?, 'ability', CURRENT_TIMESTAMP)''',
              (key, value))
    
    conn.commit()
    conn.close()
    
    return {"status": "stored", "ability": ability, "description": description}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: store_ability.py 'Ability Name' 'Description'"}, indent=2))
        sys.exit(1)
    
    ability = sys.argv[1]
    description = sys.argv[2]
    
    result = store_ability(ability, description)
    print(json.dumps(result, indent=2))
