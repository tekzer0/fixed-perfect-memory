#!/usr/bin/env python3
"""
Initialize Claude's Perfect Memory System
Sets up database schema and directory structure
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime

# Base paths
MEMORY_ROOT = Path("/mnt/s/fixed-perfect-memory")
DB_PATH = MEMORY_ROOT / "database" / "memory.db"
SCHEMA_PATH = MEMORY_ROOT / "database" / "schema.sql"

# Required directories
DIRECTORIES = [
    MEMORY_ROOT / "chats",
    MEMORY_ROOT / "entities" / "person",
    MEMORY_ROOT / "entities" / "project",
    MEMORY_ROOT / "entities" / "concept",
    MEMORY_ROOT / "entities" / "organization",
    MEMORY_ROOT / "short-term",
    MEMORY_ROOT / "images",
    MEMORY_ROOT / "embeddings",
    MEMORY_ROOT / "database"
]

def create_directories():
    """Create all required directories."""
    print("Creating directory structure...")
    for directory in DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}")
    print()

def initialize_database():
    """Initialize the SQLite database with schema."""
    print("Initializing database...")
    
    if not SCHEMA_PATH.exists():
        print(f"  ✗ Schema file not found: {SCHEMA_PATH}")
        return False
    
    try:
        conn = sqlite3.connect(DB_PATH)
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        
        # Verify tables were created
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"  ✓ Database created: {DB_PATH}")
        print(f"  ✓ Tables created: {', '.join(tables)}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ✗ Database initialization failed: {e}")
        return False

def verify_setup():
    """Verify the setup is complete."""
    print("\nVerifying setup...")
    
    checks = [
        ("Database file exists", DB_PATH.exists()),
        ("Schema file exists", SCHEMA_PATH.exists()),
        ("Chats directory exists", (MEMORY_ROOT / "chats").exists()),
        ("Entities directory exists", (MEMORY_ROOT / "entities").exists()),
        ("Database has tables", DB_PATH.exists())
    ]
    
    all_passed = True
    for check_name, passed in checks:
        status = "✓" if passed else "✗"
        print(f"  {status} {check_name}")
        all_passed = all_passed and passed
    
    if all_passed:
        # Count tables
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        table_count = cursor.fetchone()[0]
        conn.close()
        
        print(f"\n✅ Perfect Memory System initialized successfully!")
        print(f"   Database: {DB_PATH}")
        print(f"   Tables: {table_count}")
        print(f"   Root: {MEMORY_ROOT}")
        return True
    else:
        print(f"\n❌ Setup incomplete. Please check errors above.")
        return False

def main():
    """Main initialization routine."""
    print("=" * 60)
    print("Claude's Perfect Memory System - Initialization")
    print("=" * 60)
    print()
    
    try:
        # Step 1: Create directories
        create_directories()
        
        # Step 2: Initialize database
        if not initialize_database():
            sys.exit(1)
        
        # Step 3: Verify setup
        if not verify_setup():
            sys.exit(1)
        
        print()
        print("Next steps:")
        print("1. The system is ready to use")
        print("2. Use load_context.py to populate from conversation history")
        print("3. Use memory_core.py functions to store new memories")
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
