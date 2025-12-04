#!/usr/bin/env python3
"""Search across all memory using full-text search."""

import sys
import json
import sqlite3
from pathlib import Path

DB_PATH = Path("/mnt/s/claude-perfect-memory/database/memory.db")

def search_memory(query: str, content_types: list = None, limit: int = 20):
    """Full-text search across all memory."""
    conn = sqlite3.connect(DB_PATH)
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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: search_memory.py 'query terms' [limit]"}, indent=2))
        sys.exit(1)
    
    query = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    
    results = search_memory(query, limit=limit)
    print(json.dumps(results, indent=2))
