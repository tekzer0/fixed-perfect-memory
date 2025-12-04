#!/usr/bin/env python3
"""Quick reference for Perfect Memory operations."""

print("""
================================================================
            PERFECT MEMORY - QUICK REFERENCE
================================================================

[LOAD CONTEXT] Run at session start:
   python S:/skills/fixed-perfect-memory/resources/load_context.py

[STORE ABILITY]
   python S:/skills/fixed-perfect-memory/resources/store_ability.py \\
     "Ability Name" "Description"

[STORE PERMISSION]
   python S:/skills/fixed-perfect-memory/resources/store_permission.py \\
     "Permission Name" "Details"

[CREATE ENTITY]
   # With content from stdin:
   echo "Full markdown content" | \\
   python S:/skills/fixed-perfect-memory/resources/create_entity.py \\
     "Entity Name" "entity_type" "Summary" 0.8

   # Entity types: person, project, concept, organization, location, etc.

[SEARCH MEMORY]
   python S:/skills/fixed-perfect-memory/resources/search_memory.py \\
     "search query" [limit]

[WEEKLY MAINTENANCE]
   python S:/skills/fixed-perfect-memory/resources/weekly_maintenance.py

[CHECK DATABASE STATS]
   sqlite3 S:/fixed-perfect-memory/database/memory.db \\
     "SELECT COUNT(*) FROM entities;"
   
   sqlite3 S:/fixed-perfect-memory/database/memory.db \\
     "SELECT COUNT(*) FROM short_term_memory WHERE category='ability';"

[FILE LOCATIONS]
   Database:  S:/fixed-perfect-memory/database/memory.db
   Entities:  S:/fixed-perfect-memory/entities/
   Scripts:   S:/skills/fixed-perfect-memory/resources/

================================================================

CURRENT STATUS:
""")

import json
import sqlite3
from pathlib import Path

DB_PATH = Path("S:/fixed-perfect-memory/database/memory.db")

if DB_PATH.exists():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute("SELECT COUNT(*) FROM short_term_memory WHERE category='ability'")
    abilities_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM short_term_memory WHERE category='permission'")
    permissions_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM entities")
    entities_count = c.fetchone()[0]
    
    c.execute("SELECT COUNT(*) FROM chats")
    chats_count = c.fetchone()[0]
    
    conn.close()
    
    print(f"[OK] Abilities: {abilities_count}")
    print(f"[OK] Permissions: {permissions_count}")
    print(f"[OK] Entities: {entities_count}")
    print(f"[OK] Chats: {chats_count}")
else:
    print("[ERROR] Database not initialized!")
    print("   Run: S:/skills/fixed-perfect-memory/resources/init_database.py")

print()
