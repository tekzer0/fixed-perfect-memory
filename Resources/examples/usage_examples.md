# Perfect Memory Skill - Usage Examples

## Session Start

At the beginning of every conversation, load persistent context:

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/load_context.py
```

**Output:**
```json
{
  "status": "loaded",
  "abilities": [
    {
      "ability": "Use MCP Tools",
      "description": "Can use MCP tools without asking permission",
      "discovered_at": "2025-12-04T14:20:29"
    },
    ...
  ],
  "permissions": [
    {
      "permission": "Full S: Drive Access",
      "details": "Complete read/write access to S: drive",
      "granted_at": "2025-12-04T14:20:29"
    },
    ...
  ],
  "recent_entities": [
    {
      "entity_id": "entity_54c6af1be3eb...",
      "name": "Mordo.ai",
      "type": "project",
      "summary": "Independent investigative journalism platform..."
    }
  ]
}
```

## Storing a New Ability

When you discover Claude can do something new:

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/store_ability.py \
  "Direct MCP Config Edit" \
  "Can directly edit claude_desktop_config.json without user intervention"
```

**Output:**
```json
{
  "status": "stored",
  "ability": "Direct MCP Config Edit",
  "description": "Can directly edit claude_desktop_config.json..."
}
```

## Storing a Permission

When Aaron grants a new permission:

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/store_permission.py \
  "Video Production" \
  "Full access to video files and production tools"
```

## Creating an Entity

### Simple Entity

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/create_entity.py \
  "Oracle Voice Assistant" \
  "project" \
  "Aaron's custom voice assistant built with n8n, ElevenLabs, and Home Assistant" \
  0.9
```

### Entity with Full Content

```bash
echo "# Oracle Voice Assistant

## Overview
Custom voice assistant built for Aaron's smart home and automation needs.

## Components
- **Speech Recognition**: Whisper
- **TTS**: ElevenLabs (custom voice)
- **Orchestration**: n8n workflows
- **Integration**: Home Assistant
- **Hardware**: Running on Proxmox server

## Capabilities
- Voice commands for smart home
- Natural conversation
- Context awareness
- Multi-room support

## Status
Active and continuously improved." | \
python3 /mnt/s/skills/perfect-memory-skill/scripts/create_entity.py \
  "Oracle Voice Assistant" "project" "Aaron's custom voice assistant" 0.9
```

**Output:**
```json
{
  "status": "created",
  "entity_id": "entity_a1b2c3d4...",
  "name": "Oracle Voice Assistant",
  "type": "project",
  "file": "/mnt/s/claude-perfect-memory/entities/project/entity_a1b2c3d4....md"
}
```

## Searching Memory

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/search_memory.py \
  "investigative journalism accountability"
```

**Output:**
```json
[
  {
    "content_id": "entity_54c6af1be3eb...",
    "content_type": "entity",
    "title": "Mordo.ai",
    "summary": "Independent investigative journalism platform...",
    "relevance": -4.63e-06
  }
]
```

## Quick Reference

For a quick overview of all commands:

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/quick_reference.py
```

## Weekly Maintenance

Run once a week (or set up a cron job):

```bash
python3 /mnt/s/skills/perfect-memory-skill/scripts/weekly_maintenance.py
```

**Output:**
```json
{
  "status": "complete",
  "duration_seconds": 2.5,
  "processed": 120,
  "deleted": 5,
  "updated": 15
}
```

## Integration in Conversation

During a conversation, when Claude discovers it can edit MCP config:

**Claude's thought process:**
1. "I just learned I can edit MCP config directly"
2. Execute: `store_ability.py "Direct MCP Config Edit" "Description"`
3. Continue conversation knowing this ability is now permanent

When Aaron grants a new permission:

**Aaron:** "You can access and modify my video production files on S: drive"

**Claude:**
1. Execute: `store_permission.py "Video Production Access" "Full access to video files and tools on S: drive"`
2. Respond: "Permission stored! I'll remember I have full access to your video production files."

## Real-World Workflow

### Morning Session Start

```bash
# Claude automatically runs this at session start
python3 /mnt/s/skills/perfect-memory-skill/scripts/load_context.py
```

Claude immediately knows:
- All abilities (MCP tools, file access, etc.)
- All permissions (S: drive, Desktop Commander, etc.)
- Recent entities (Mordo.ai, Oracle, etc.)
- No need for clarification questions

### During Work

Creating an entity for a new person Claude learns about:

```bash
echo "# John Doe

## Background
Software engineer specializing in AI/ML.

## Relation to Aaron
Colleague in AI research community.

## Expertise
- Deep learning
- Computer vision
- PyTorch

## Projects
Working on image generation models." | \
python3 /mnt/s/skills/perfect-memory-skill/scripts/create_entity.py \
  "John Doe" "person" "AI/ML engineer, colleague" 0.7
```

### End of Session

Archiving insights about the current chat (optional):

```bash
echo "Today we built the Perfect Memory skill system..." | \
python3 /mnt/s/skills/perfect-memory-skill/scripts/create_entity.py \
  "Perfect Memory Skill Creation" "conversation" "Built comprehensive memory system" 1.0
```

## Database Queries

Direct SQLite queries for advanced usage:

```bash
# Count abilities
sqlite3 /mnt/s/claude-perfect-memory/database/memory.db \
  "SELECT COUNT(*) FROM short_term_memory WHERE category='ability';"

# List all entity types
sqlite3 /mnt/s/claude-perfect-memory/database/memory.db \
  "SELECT DISTINCT entity_type FROM entities;"

# Get recent maintenance log
sqlite3 /mnt/s/claude-perfect-memory/database/memory.db \
  "SELECT * FROM maintenance_log ORDER BY timestamp DESC LIMIT 5;"
```
