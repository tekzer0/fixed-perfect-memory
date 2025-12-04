#!/usr/bin/env python3
"""
Claude's Perfect Memory MCP Server
Provides comprehensive, flawless memory persistence across all sessions.
"""

import json
import sqlite3
import hashlib
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Any
import uuid

# Base paths
MEMORY_ROOT = Path("S:/fixed-perfect-memory")
DB_PATH = MEMORY_ROOT / "database" / "memory.db"
CHATS_DIR = MEMORY_ROOT / "chats"
ENTITIES_DIR = MEMORY_ROOT / "entities"
SHORT_TERM_DIR = MEMORY_ROOT / "short-term"
IMAGES_DIR = MEMORY_ROOT / "images"
EMBEDDINGS_DIR = MEMORY_ROOT / "embeddings"

# Ensure directories exist
for dir_path in [CHATS_DIR, ENTITIES_DIR, SHORT_TERM_DIR, IMAGES_DIR, EMBEDDINGS_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

def init_database():
    """Initialize the SQLite database with schema."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Short-term memory for abilities and permissions
    c.execute('''CREATE TABLE IF NOT EXISTS short_term_memory (
        key TEXT PRIMARY KEY,
        value TEXT NOT NULL,
        category TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Chat transcripts index
    c.execute('''CREATE TABLE IF NOT EXISTS chats (
        chat_id TEXT PRIMARY KEY,
        url TEXT,
        title TEXT NOT NULL,
        summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        tools_used TEXT,
        topics TEXT,
        file_path TEXT NOT NULL
    )''')
    
    # Entity storage
    c.execute('''CREATE TABLE IF NOT EXISTS entities (
        entity_id TEXT PRIMARY KEY,
        entity_type TEXT NOT NULL,
        name TEXT NOT NULL,
        summary TEXT,
        file_path TEXT NOT NULL,
        importance_score REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Relations between entities
    c.execute('''CREATE TABLE IF NOT EXISTS relations (
        relation_id INTEGER PRIMARY KEY AUTOINCREMENT,
        from_entity_id TEXT NOT NULL,
        to_entity_id TEXT NOT NULL,
        relation_type TEXT NOT NULL,
        strength REAL DEFAULT 0.5,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (from_entity_id) REFERENCES entities(entity_id),
        FOREIGN KEY (to_entity_id) REFERENCES entities(entity_id)
    )''')
    
    # Full-text search index
    c.execute('''CREATE VIRTUAL TABLE IF NOT EXISTS memory_search USING fts5(
        content_id,
        content_type,
        title,
        summary,
        content
    )''')
    
    # Memory access tracking
    c.execute('''CREATE TABLE IF NOT EXISTS memory_index (
        content_id TEXT PRIMARY KEY,
        content_type TEXT NOT NULL,
        importance_score REAL DEFAULT 0.5,
        access_count INTEGER DEFAULT 0,
        last_accessed TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    # Maintenance log
    c.execute('''CREATE TABLE IF NOT EXISTS maintenance_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        operation TEXT NOT NULL,
        items_processed INTEGER DEFAULT 0,
        items_deleted INTEGER DEFAULT 0,
        items_updated INTEGER DEFAULT 0,
        duration_seconds REAL,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )''')
    
    conn.commit()
    conn.close()

def get_connection():
    """Get database connection."""
    return sqlite3.connect(DB_PATH)

def generate_id(prefix: str = "") -> str:
    """Generate unique ID."""
    return f"{prefix}{uuid.uuid4().hex}"

def calculate_hash(content: str) -> str:
    """Calculate content hash for embeddings."""
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

# ==================== SHORT-TERM MEMORY ====================

def store_ability(ability: str, description: str):
    """Store a discovered ability in persistent memory."""
    conn = get_connection()
    c = conn.cursor()
    
    key = f"ability_{ability.lower().replace(' ', '_')}"
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
    
    return {"status": "stored", "ability": ability}

def store_permission(permission: str, details: str):
    """Store a granted permission in persistent memory."""
    conn = get_connection()
    c = conn.cursor()
    
    key = f"permission_{permission.lower().replace(' ', '_')}"
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
    
    return {"status": "stored", "permission": permission}

def get_all_abilities() -> List[Dict]:
    """Get all stored abilities."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT key, value FROM short_term_memory WHERE category = 'ability' ''')
    abilities = []
    
    for row in c.fetchall():
        abilities.append(json.loads(row[1]))
    
    conn.close()
    return abilities

def get_all_permissions() -> List[Dict]:
    """Get all stored permissions."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT key, value FROM short_term_memory WHERE category = 'permission' ''')
    permissions = []
    
    for row in c.fetchall():
        permissions.append(json.loads(row[1]))
    
    conn.close()
    return permissions

# ==================== CHAT STORAGE ====================

def store_chat(chat_id: str, url: str, title: str, content: str, 
               summary: str = "", tools_used: List[str] = None, 
               topics: List[str] = None) -> Dict:
    """Store a complete chat transcript."""
    
    # Store full content in file
    chat_file = CHATS_DIR / f"{chat_id}.md"
    with open(chat_file, 'w', encoding='utf-8') as f:
        f.write(f"# {title}\n\n")
        f.write(f"**URL:** {url}\n\n")
        f.write(f"**Date:** {datetime.now().isoformat()}\n\n")
        f.write("---\n\n")
        f.write(content)
    
    # Store index in database
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''INSERT OR REPLACE INTO chats 
                 (chat_id, url, title, summary, updated_at, tools_used, topics, file_path)
                 VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, ?, ?, ?)''',
              (chat_id, url, title, summary, 
               json.dumps(tools_used or []), 
               json.dumps(topics or []),
               str(chat_file)))
    
    # Add to full-text search
    c.execute('''INSERT INTO memory_search (content_id, content_type, title, summary, content)
                 VALUES (?, 'chat', ?, ?, ?)''',
              (chat_id, title, summary, content[:10000]))  # Limit content for FTS
    
    conn.commit()
    conn.close()
    
    return {"status": "stored", "chat_id": chat_id, "file": str(chat_file)}

# ==================== ENTITY STORAGE ====================

def create_entity(name: str, entity_type: str, content: str, 
                 summary: str = "", importance: float = 0.5) -> Dict:
    """Create or update an entity with full details."""
    
    entity_id = generate_id("entity_")
    
    # Store full content in markdown file
    entity_file = ENTITIES_DIR / entity_type / f"{entity_id}.md"
    entity_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(entity_file, 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n\n")
        f.write(f"**Type:** {entity_type}\n")
        f.write(f"**Created:** {datetime.now().isoformat()}\n\n")
        f.write("---\n\n")
        f.write(content)
    
    # Store index in database
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''INSERT INTO entities (entity_id, entity_type, name, summary, file_path, importance_score)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (entity_id, entity_type, name, summary, str(entity_file), importance))
    
    # Add to full-text search
    c.execute('''INSERT INTO memory_search (content_id, content_type, title, summary, content)
                 VALUES (?, 'entity', ?, ?, ?)''',
              (entity_id, name, summary, content[:10000]))
    
    conn.commit()
    conn.close()
    
    return {"status": "created", "entity_id": entity_id, "name": name, "file": str(entity_file)}

def update_entity(entity_id: str, new_content: str, append: bool = True) -> Dict:
    """Update an existing entity."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('SELECT file_path FROM entities WHERE entity_id = ?', (entity_id,))
    result = c.fetchone()
    
    if not result:
        conn.close()
        return {"status": "error", "message": "Entity not found"}
    
    file_path = Path(result[0])
    
    if append:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n---\n\n**Updated:** {datetime.now().isoformat()}\n\n")
            f.write(new_content)
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    c.execute('UPDATE entities SET updated_at = CURRENT_TIMESTAMP WHERE entity_id = ?', (entity_id,))
    conn.commit()
    conn.close()
    
    return {"status": "updated", "entity_id": entity_id}

def create_relation(from_entity: str, to_entity: str, relation_type: str, strength: float = 0.5) -> Dict:
    """Create a relation between two entities."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''INSERT INTO relations (from_entity_id, to_entity_id, relation_type, strength)
                 VALUES (?, ?, ?, ?)''',
              (from_entity, to_entity, relation_type, strength))
    
    relation_id = c.lastrowid
    conn.commit()
    conn.close()
    
    return {"status": "created", "relation_id": relation_id}

# ==================== SEARCH & RETRIEVAL ====================

def search_memory(query: str, content_types: List[str] = None, limit: int = 20) -> List[Dict]:
    """Full-text search across all memory."""
    conn = get_connection()
    c = conn.cursor()
    
    if content_types:
        type_filter = " AND content_type IN ({})".format(','.join('?' * len(content_types)))
        c.execute(f'''SELECT content_id, content_type, title, summary, rank
                     FROM memory_search 
                     WHERE memory_search MATCH ?{type_filter}
                     ORDER BY rank
                     LIMIT ?''',
                  [query] + content_types + [limit])
    else:
        c.execute('''SELECT content_id, content_type, title, summary, rank
                     FROM memory_search 
                     WHERE memory_search MATCH ?
                     ORDER BY rank
                     LIMIT ?''',
                  (query, limit))
    
    results = []
    for row in c.fetchall():
        results.append({
            "content_id": row[0],
            "content_type": row[1],
            "title": row[2],
            "summary": row[3],
            "relevance": row[4]
        })
    
    conn.close()
    return results

def get_entity(entity_id: str) -> Dict:
    """Get full entity details."""
    conn = get_connection()
    c = conn.cursor()
    
    c.execute('''SELECT entity_id, entity_type, name, summary, file_path, 
                        importance_score, created_at, updated_at
                 FROM entities WHERE entity_id = ?''', (entity_id,))
    
    row = c.fetchone()
    conn.close()
    
    if not row:
        return {"status": "error", "message": "Entity not found"}
    
    file_path = Path(row[4])
    content = file_path.read_text(encoding='utf-8') if file_path.exists() else ""
    
    return {
        "entity_id": row[0],
        "entity_type": row[1],
        "name": row[2],
        "summary": row[3],
        "importance": row[5],
        "created_at": row[6],
        "updated_at": row[7],
        "content": content
    }

# ==================== WEEKLY MAINTENANCE ====================

def weekly_maintenance() -> Dict:
    """Perform weekly curation and maintenance."""
    start_time = datetime.now()
    conn = get_connection()
    c = conn.cursor()
    
    stats = {
        "processed": 0,
        "deleted": 0,
        "updated": 0
    }
    
    # 1. Remove low-importance, old, unaccessed items
    cutoff_date = (datetime.now() - timedelta(days=90)).isoformat()
    c.execute('''DELETE FROM memory_index 
                 WHERE importance_score < 0.2 
                 AND last_accessed < ? 
                 AND access_count < 3''',
              (cutoff_date,))
    stats["deleted"] += c.rowcount
    
    # 2. Update importance scores based on access patterns
    c.execute('''UPDATE memory_index 
                 SET importance_score = MIN(1.0, importance_score + (access_count * 0.01))
                 WHERE access_count > 0''')
    stats["updated"] += c.rowcount
    
    # 3. Clean up orphaned files
    # (Check database vs actual files and remove orphans)
    
    # 4. Rebuild full-text search index
    c.execute('DELETE FROM memory_search')
    
    # Re-index chats
    c.execute('SELECT chat_id, title, summary, file_path FROM chats')
    for row in c.fetchall():
        file_path = Path(row[3])
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')[:10000]
            c.execute('''INSERT INTO memory_search (content_id, content_type, title, summary, content)
                         VALUES (?, 'chat', ?, ?, ?)''',
                      (row[0], row[1], row[2], content))
            stats["processed"] += 1
    
    # Re-index entities
    c.execute('SELECT entity_id, name, summary, file_path FROM entities')
    for row in c.fetchall():
        file_path = Path(row[3])
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')[:10000]
            c.execute('''INSERT INTO memory_search (content_id, content_type, title, summary, content)
                         VALUES (?, 'entity', ?, ?, ?)''',
                      (row[0], row[1], row[2], content))
            stats["processed"] += 1
    
    duration = (datetime.now() - start_time).total_seconds()
    
    # Log maintenance
    c.execute('''INSERT INTO maintenance_log 
                 (operation, items_processed, items_deleted, items_updated, duration_seconds)
                 VALUES ('weekly_curation', ?, ?, ?, ?)''',
              (stats["processed"], stats["deleted"], stats["updated"], duration))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "complete",
        "duration_seconds": duration,
        **stats
    }

# ==================== INITIALIZATION ====================

def initialize_database():
    """Initialize database schema and default abilities/permissions."""
    init_database()
    initialize_abilities_and_permissions()
    return {
        "status": "initialized",
        "database": str(DB_PATH)
    }

def initialize_abilities_and_permissions():
    """Initialize known abilities and permissions on first run."""
    abilities = [
        ("Use MCP Tools", "Can use MCP tools without asking permission"),
        ("Create Files on S: Drive", "Default workspace is S: drive for all collaboration"),
        ("Access Past Chats", "Can search and retrieve past conversations automatically"),
        ("Incremental Context", "Maintains fresh context via Robinson Context Engine"),
        ("Memory Persistence", "Has flawless persistent memory across all sessions"),
        ("Proactive Tool Use", "Uses tools proactively when needed, no permission required")
    ]
    
    permissions = [
        ("Full S: Drive Access", "Complete read/write access to S: drive"),
        ("Desktop Commander", "Can use Desktop Commander for system operations"),
        ("Filesystem Access", "Can read/write files in authorized directories"),
        ("Web Search", "Can search the web for current information"),
        ("Code Execution", "Can execute code for analysis and automation")
    ]
    
    for ability, desc in abilities:
        store_ability(ability, desc)
    
    for permission, details in permissions:
        store_permission(permission, details)

# ==================== MAIN ====================

if __name__ == "__main__":
    print("Initializing Claude's Perfect Memory System...")
    init_database()
    initialize_abilities_and_permissions()
    print("✅ Memory system initialized!")
    print(f"📁 Database: {DB_PATH}")
    print(f"📁 Storage root: {MEMORY_ROOT}")
