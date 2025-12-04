#!/usr/bin/env python3
"""Create a detailed entity with full markdown content."""

import sys
import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path("S:/fixed-perfect-memory/database/memory.db")
ENTITIES_DIR = Path("S:/fixed-perfect-memory/entities")

def create_entity(name: str, entity_type: str, summary: str = "", importance: float = 0.5):
    """Create an entity. Content should be provided via stdin for full markdown."""
    
    # Read full content from stdin if available
    content = sys.stdin.read() if not sys.stdin.isatty() else ""
    
    entity_id = f"entity_{uuid.uuid4().hex}"
    
    # Create entity file
    entity_dir = ENTITIES_DIR / entity_type
    entity_dir.mkdir(parents=True, exist_ok=True)
    entity_file = entity_dir / f"{entity_id}.md"
    
    with open(entity_file, 'w', encoding='utf-8') as f:
        f.write(f"# {name}\n\n")
        f.write(f"**Type:** {entity_type}\n")
        f.write(f"**Created:** {datetime.now().isoformat()}\n\n")
        if summary:
            f.write(f"**Summary:** {summary}\n\n")
        f.write("---\n\n")
        if content:
            f.write(content)
        else:
            f.write(f"# {name}\n\nDetails to be added.\n")
    
    # Store in database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''INSERT INTO entities (entity_id, entity_type, name, summary, file_path, importance_score)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (entity_id, entity_type, name, summary, str(entity_file), importance))
    
    # Add to full-text search
    c.execute('''INSERT INTO memory_search (content_id, content_type, title, summary, content)
                 VALUES (?, 'entity', ?, ?, ?)''',
              (entity_id, name, summary, content[:10000] if content else name))
    
    conn.commit()
    conn.close()
    
    return {
        "status": "created",
        "entity_id": entity_id,
        "name": name,
        "type": entity_type,
        "file": str(entity_file)
    }

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(json.dumps({
            "error": "Usage: create_entity.py 'Name' 'type' ['summary'] [importance]",
            "example": "echo 'Full markdown content' | create_entity.py 'Project Name' 'project' 'Brief summary' 0.8"
        }, indent=2))
        sys.exit(1)
    
    name = sys.argv[1]
    entity_type = sys.argv[2]
    summary = sys.argv[3] if len(sys.argv) > 3 else ""
    importance = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
    
    result = create_entity(name, entity_type, summary, importance)
    print(json.dumps(result, indent=2))
