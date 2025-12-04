#!/usr/bin/env python3
"""Store a granted permission in persistent memory."""

import sys
import json
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path("/mnt/s/claude-perfect-memory/database/memory.db")

def store_permission(permission: str, details: str):
    """Store a permission."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    key = f"permission_{permission.lower().replace(' ', '_').replace('-', '_')}"
    value = json.dumps({
        "permission": permission,
        "details": details,
        "granted_at": datetime.now().isoformat()
    })
    
    c.execute('''INSERT OR REPLACE INTO short_term_memory (key, value, category, updated_at)
                 VALUES (?, ?, 'permission', CURRENT_TIMESTAMP)''',
              (key, value))
    
    conn.commit()
    conn.close()
    
    return {"status": "stored", "permission": permission, "details": details}

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({"error": "Usage: store_permission.py 'Permission Name' 'Details'"}, indent=2))
        sys.exit(1)
    
    permission = sys.argv[1]
    details = sys.argv[2]
    
    result = store_permission(permission, details)
    print(json.dumps(result, indent=2))
