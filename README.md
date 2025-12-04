# Perfect Memory Skill for Claude

**Give Claude flawless, persistent memory across all conversations** - No configuration, no MCP server, just perfect recall.

[![License: Non-Commercial](https://img.shields.io/badge/License-Non--Commercial-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/tekzer0/fixed-perfect-memory)

## What Is This?

A self-contained skill that gives Claude:

- ✅ **Perfect Recall** - Never forgets abilities or permissions
- ✅ **Complete Archives** - Full transcripts of every conversation
- ✅ **Deep Understanding** - Detailed entity files for people, projects, concepts
- ✅ **Instant Search** - Find anything across all memory
- ✅ **Auto-Curation** - Weekly maintenance keeps everything optimized
- ✅ **Zero Setup** - Install once, works forever

## Why This Exists

Claude is brilliant, but it forgets everything between sessions:
- "Can I use MCP tools?" (You already said yes!)
- "Do I have access to that folder?" (Yes, you granted permission!)
- "What were we working on?" (We discussed this yesterday!)

**This skill solves that.** Install it once, and Claude remembers everything forever.

## Quick Start

### 1. Download the Skill & Clone the repo

Download `fixed-perfect-memory.zip` from the [releases page](https://github.com/yourusername/claude-perfect-memory/releases).

```bash
git clone https://github.com/tekzer0/fixed-perfect-memory.git

### 2. Install in Claude Desktop

**Option A: Via UI (Recommended)**
1. Open Claude Desktop
2. Go to Settings → Skills
3. Click "Install Skill"
4. Select the downloaded `.skill` file
5. Done!

**Option B: Manual**
```bash
# Copy to Claude skills directory
cp fixed-perfect-memory.zip ~/Library/Application\ Support/Claude/skills/
# Restart Claude Desktop
```

### 3. Initialize Database

First time only:
```bash
cd /path/to/skill/installation
python3 /fixed-perfect-memory/resources/initialize.py
```

### 4. It Just Works

From the next conversation, Claude will:
- Auto-load all abilities and permissions
- Remember everything discovered
- Search across all past conversations
- Never need reminders again

## What Gets Remembered

**Automatically Stored:**
- ✅ Abilities (every capability Claude discovers)
- ✅ Permissions (every authorization you grant)
- ✅ Chats (complete transcripts with context)
- ✅ Entities (people, projects, concepts - detailed files)
- ✅ Relations (how entities connect)
- ✅ Images (visual content and references)
- ✅ Everything Claude comprehends

**Never Stored:**
- ❌ Items marked for deletion
- ❌ Data errors
- ❌ Broken/incomplete code
- ❌ Invalid data

## Features

### Persistent Short-Term Memory

Claude never forgets:
```json
{
  "abilities": [
    "Use MCP Tools without asking",
    "Full /fixed-perfect-memory/ folder access",
    "Access past chats automatically",
    ...
  ],
  "permissions": [
    "Desktop Commander access",
    "Code execution",
    "Web search",
    ...
  ]
}
```

### Individual Entity Files

Detailed markdown files for everything:
```
entities/
├── person/
│   ├── entity_abc123.md  # Full person profile
│   └── entity_def456.md
├── project/
│   ├── entity_ghi789.md  # Complete project details
│   └── entity_jkl012.md
└── concept/
    └── entity_mno345.md  # In-depth concept explanation
```

### Full-Text Search

Find anything instantly:
```bash
python3 scripts/search_memory.py "investigative journalism"
```

### Weekly Auto-Curation

Keeps memory optimized:
- Removes low-value old content
- Updates importance scores
- Rebuilds search indexes
- Logs all operations

## How It Works

### At Session Start (Automatic)

```bash
# Claude automatically runs:
python3 scripts/load_context.py
```

Output loads directly into Claude's context:
```json
{
  "status": "loaded",
  "abilities": [...],
  "permissions": [...],
  "recent_entities": [...]
}
```

### During Conversations

Claude can execute scripts directly:

**Store New Ability:**
```bash
python3 scripts/store_ability.py "Ability Name" "Description"
```

**Create Entity:**
```bash
echo "Full markdown content" | \
python3 scripts/create_entity.py "Name" "type" "Summary" 0.8
```

**Search:**
```bash
python3 scripts/search_memory.py "query terms"
```

## Architecture

### Database (SQLite)

```
/fixed-perfect-memory/database/memory.db
```

**Tables:**
- `short_term_memory` - Abilities, permissions, persistent context
- `entities` - Entity index with importance scoring
- `chats` - Chat transcript metadata
- `relations` - Entity relationship graph
- `images` - Visual content index
- `embeddings` - Cached vectors for semantic search
- `memory_search` - FTS5 full-text search

### File Storage

```
/fixed-perfect-memory/
├── database/
│   └── memory.db
├── chats/           # Full transcripts (markdown)
├── entities/        # Detailed entity files
│   ├── person/
│   ├── project/
│   ├── concept/
│   └── organization/
├── images/          # Visual content
└── embeddings/      # Cached vectors
```

## Examples

See [examples/usage_examples.md](examples/usage_examples.md) for comprehensive usage examples.

### Quick Reference

```bash
# Load context at session start
python3 scripts/load_context.py

# Store ability
python3 scripts/store_ability.py "New Ability" "What it does"

# Store permission
python3 scripts/store_permission.py "Permission" "Details"

# Create entity
echo "Content" | python3 scripts/create_entity.py "Name" "type" "Summary" 0.8

# Search memory
python3 scripts/search_memory.py "search query"

# Weekly maintenance
python3 scripts/weekly_maintenance.py

# Quick help
python3 scripts/quick_reference.py
```

## Benefits

### For Users

- **Save Time** - No more repeating permissions and abilities
- **Maintain Context** - Every conversation builds on the last
- **Deep Understanding** - Claude knows your projects, people, concepts
- **Fast Access** - Search finds anything instantly

### For Claude

- **No Confusion** - Always knows what it can do
- **Complete Context** - Never loses track of ongoing work
- **Efficient** - No wasted tokens on repeated clarifications
- **Growing Knowledge** - Learns and remembers continuously

## Requirements

- Python 3.7+
- SQLite3
- Claude Desktop with skills support
- ~20MB storage for database

## File Structure

```
fixed-perfect-memory/
├── SKILL.md                 # Skill definition
├── LICENSE                  # Non-commercial license
├── README.md                # This file
├── scripts/
│   ├── load_context.py      # Auto-load at start
│   ├── store_ability.py
│   ├── store_permission.py
│   ├── create_entity.py
│   ├── search_memory.py
│   ├── weekly_maintenance.py
│   ├── quick_reference.py
│   └── memory_core.py       # Core functions
├── examples/
│   └── usage_examples.md
└── references/
    └── integration.md
```

## Comparison

| Feature | Default Claude | With Perfect Memory |
|---------|----------------|---------------------|
| Remembers abilities | ❌ No | ✅ Forever |
| Remembers permissions | ❌ No | ✅ Forever |
| Chat history | 🟡 Recent only | ✅ Complete archive |
| Entity details | 🟡 Basic observations | ✅ Full markdown files |
| Search | ❌ No | ✅ Full-text + semantic |
| Maintenance | ❌ Manual | ✅ Auto-curation |
| Setup required | ✅ None | ✅ Install once |

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For major changes, please open an issue first.

## License

**Non-Commercial Use Only**

Free for personal, educational, and non-profit use.  
Commercial licensing available - contact for details.

See [LICENSE](LICENSE) for full terms.

## Credits

Created by tekzer0 to give Claude flawless memory and make AI assistants more helpful for everyone.

Built with the goal of making the world a little bit better, one conversation at a time.

## Support

- **Issues**: [GitHub Issues](https://github.com/tekzer0/fixed-perfect-memory/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tekzer0/fixed-perfect-memory/discussions)

## Changelog

### v1.0.0 (2025-12-04)
- Initial release
- Persistent abilities and permissions
- Complete chat archive
- Individual entity files
- Full-text search
- Weekly auto-curation
- Zero configuration required

---

**Made with ❤️ to help Claude remember everything and help everyone spend more time making the world better.**
