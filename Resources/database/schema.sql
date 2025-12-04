-- Claude's Perfect Memory Database Schema
-- Provides comprehensive memory persistence across all sessions

-- Short-term memory for abilities, permissions, and session context
CREATE TABLE IF NOT EXISTS short_term_memory (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    category TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat transcripts index
CREATE TABLE IF NOT EXISTS chats (
    chat_id TEXT PRIMARY KEY,
    url TEXT NOT NULL,
    title TEXT NOT NULL,
    summary TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tools_used TEXT,  -- JSON array
    topics TEXT,      -- JSON array
    file_path TEXT NOT NULL
);

-- Entity storage (people, projects, concepts, etc.)
CREATE TABLE IF NOT EXISTS entities (
    entity_id TEXT PRIMARY KEY,
    entity_type TEXT NOT NULL,
    name TEXT NOT NULL,
    summary TEXT,
    file_path TEXT NOT NULL,
    importance_score REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Relations between entities
CREATE TABLE IF NOT EXISTS relations (
    relation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_entity_id TEXT NOT NULL,
    to_entity_id TEXT NOT NULL,
    relation_type TEXT NOT NULL,
    strength REAL DEFAULT 0.5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (from_entity_id) REFERENCES entities(entity_id),
    FOREIGN KEY (to_entity_id) REFERENCES entities(entity_id)
);

-- Full-text search virtual table
CREATE VIRTUAL TABLE IF NOT EXISTS memory_search USING fts5(
    content_id,
    content_type,
    title,
    summary,
    content,
    tokenize = 'porter unicode61'
);

-- Memory index for embeddings
CREATE TABLE IF NOT EXISTS memory_index (
    index_id INTEGER PRIMARY KEY AUTOINCREMENT,
    content_id TEXT NOT NULL,
    content_type TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    content_hash TEXT NOT NULL,
    embedding_path TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(content_id, chunk_index)
);

-- Maintenance log
CREATE TABLE IF NOT EXISTS maintenance_log (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation TEXT NOT NULL,
    status TEXT NOT NULL,
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_short_term_category ON short_term_memory(category);
CREATE INDEX IF NOT EXISTS idx_chats_updated ON chats(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);
CREATE INDEX IF NOT EXISTS idx_entities_importance ON entities(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_relations_from ON relations(from_entity_id);
CREATE INDEX IF NOT EXISTS idx_relations_to ON relations(to_entity_id);
CREATE INDEX IF NOT EXISTS idx_memory_index_content ON memory_index(content_id);
