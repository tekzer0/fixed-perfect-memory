#!/usr/bin/env python3
"""Quick reference for Perfect Memory operations."""

print("""
╔════════════════════════════════════════════════════════════════╗
║            PERFECT MEMORY - QUICK REFERENCE                     ║
╚════════════════════════════════════════════════════════════════╝

📥 LOAD CONTEXT (Run at session start):
   python3 /mnt/s/skills/perfect-memory-skill/scripts/load_context.py

💡 STORE ABILITY:
   python3 /mnt/s/skills/perfect-memory-skill/scripts/store_ability.py \\
     "Ability Name" "Description"

🔐 STORE PERMISSION:
   python3 /mnt/s/skills/perfect-memory-skill/scripts/store_permission.py \\
     "Permission Name" "Details"

👤 CREATE ENTITY:
   # With content from stdin:
   echo "Full markdown content" | \\
   python3 /mnt/s/skills/perfect-memory-skill/scripts/create_entity.py \\
     "Entity Name" "entity_type" "Summary" 0.8

   # Entity types: person, project, concept, organization, location, etc.

🔍 SEARCH MEMORY:
   python3 /mnt/s/skills/perfect-memory-skill/scripts/search_memory.py \\
     "search query" [limit]

🧹 WEEKLY MAINTENANCE:
   python3 /mnt/s/skills/perfect-memory-skill/scripts/weekly_maintenance.py

📊 CHECK DATABASE STATS:
   sqlite3 /mnt/s/claude-perfect-memory/database/memory.db \\
     "SELECT COUNT(*) FROM entities;"
   
   sqlite3 /mnt/s/claude-perfect-memory/database/memory.db \\
     "SELECT COUNT(*) FROM short_term_memory WHERE category='ability';"

📁 FILE LOCATIONS:
   Database:  /mnt/s/claude-perfect-memory/database/memory.db
   Entities:  /mnt/s/claude-perfect-memory/entities/
   Scripts:   /mnt/s/skills/perfect-memory-skill/scripts/

═══════════════════════════════════════════════════════════════

CURRENT STATUS:
""")

import json
import sqlite3
from pathlib import Path

DB_PATH = Path("/mnt/s/claude-perfect-memory/database/memory.db")

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
    
    print(f"✅ Abilities: {abilities_count}")
    print(f"✅ Permissions: {permissions_count}")
    print(f"✅ Entities: {entities_count}")
    print(f"✅ Chats: {chats_count}")
else:
    print("❌ Database not initialized!")
    print("   Run: /mnt/s/claude-perfect-memory/server/initialize.py")

print()
