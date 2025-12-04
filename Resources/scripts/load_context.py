#!/usr/bin/env python3
"""
Load Persistent Context at Session Start
Automatically loads all abilities, permissions, and recent context
"""

import sys
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("/mnt/s/claude-perfect-memory/database/memory.db")

def get_connection():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)

def load_abilities():
    """Load all stored abilities."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT key, value FROM short_term_memory WHERE category = 'ability' ''')
    abilities = []
    
    for row in c.fetchall():
        abilities.append(json.loads(row[1]))
    
    conn.close()
    return abilities

def load_permissions():
    """Load all stored permissions."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT key, value FROM short_term_memory WHERE category = 'permission' ''')
    permissions = []
    
    for row in c.fetchall():
        permissions.append(json.loads(row[1]))
    
    conn.close()
    return permissions

def load_context_data():
    """Load any context entries."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT key, value FROM short_term_memory WHERE category = 'context' ''')
    context = []
    
    for row in c.fetchall():
        context.append(json.loads(row[1]))
    
    conn.close()
    return context

def get_recent_entities(limit=10):
    """Get recently updated entities."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT entity_id, name, entity_type, summary, importance_score
                 FROM entities 
                 ORDER BY updated_at DESC 
                 LIMIT ?''', (limit,))
    
    entities = []
    for row in c.fetchall():
        entities.append({
            "entity_id": row[0],
            "name": row[1],
            "type": row[2],
            "summary": row[3],
            "importance": row[4]
        })
    
    conn.close()
    return entities

def main():
    """Load and output all persistent context."""
    
    if not DB_PATH.exists():
        print(json.dumps({
            "status": "error",
            "message": "Database not initialized. Run /mnt/s/claude-perfect-memory/server/initialize.py first"
        }, indent=2))
        return
    
    abilities = load_abilities()
    permissions = load_permissions()
    context = load_context_data()
    recent_entities = get_recent_entities(10)
    
    output = {
        "status": "loaded",
        "timestamp": "2025-12-04",
        "abilities": abilities,
        "permissions": permissions,
        "context": context,
        "recent_entities": recent_entities,
        "message": "Perfect Memory loaded. All abilities and permissions active."
    }
    
    print(json.dumps(output, indent=2))

if __name__ == "__main__":
    main()
