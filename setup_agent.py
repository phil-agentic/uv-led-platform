import os
import sqlite3
from datetime import datetime
from pathlib import Path

def initialize_environment():
    # 1. Create Directory Structure
    print("Creating directories...")
    
    # Check for system prompt file
    if Path("gemini.md").exists():
        print("Found gemini.md (System Prompt).")
    elif Path("CLAUDE.md").exists():
        print("Found CLAUDE.md (System Prompt).")
    else:
        print("\n⚠️  WARNING: No system prompt file (gemini.md or CLAUDE.md) found!")
        print("   The agent requires this file to understand its instructions.\n")

    # Check for required tool scripts
    required_tools = [
        "tools/memory/memory_read.py",
        "tools/memory/memory_write.py"
    ]
    missing_tools = [t for t in required_tools if not Path(t).exists()]
    if missing_tools:
        print("\n⚠️  WARNING: Missing required tool scripts!")
        for t in missing_tools:
            print(f"   - {t}")
        print("   The agent will fail without these. Please download the 'memory' folder")
        print("   and place it inside a 'tools' folder as per SETUP_GUIDE.md Step 5.\n")

    Path("memory/logs").mkdir(parents=True, exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    
    # 2. Create MEMORY.md
    memory_file = Path("memory/MEMORY.md")
    if not memory_file.exists():
        print("Creating memory/MEMORY.md...")
        memory_content = """# Persistent Memory

> This file contains curated long-term facts, preferences, and context that persist across sessions.
> The AI reads this at the start of each session. You can edit this file directly.

## User Preferences

- (Add your preferences here)

## Key Facts

- (Add key facts about your work/projects)

## Learned Behaviors

- Always check tools/manifest.md before creating new scripts
- Follow GOTCHA framework: Goals, Orchestration, Tools, Context, Hardprompts, Args

## Current Projects

- (List active projects)

## Technical Context

- Framework: GOTCHA (6-layer agentic architecture)

---

*Last updated: {date}*
*This file is the source of truth for persistent facts. Edit directly to update.*
""".format(date=datetime.now().strftime("%Y-%m-%d"))
        
        with open(memory_file, "w", encoding="utf-8") as f:
            f.write(memory_content)
    else:
        print("memory/MEMORY.md already exists.")

    # 3. Create Today's Log
    today_str = datetime.now().strftime("%Y-%m-%d")
    log_file = Path(f"memory/logs/{today_str}.md")
    
    print(f"Creating daily log: {log_file}...")
    log_content = f"""# Daily Log: {today_str}

> Session log for {datetime.now().strftime('%A, %B %d, %Y')}

---

## Events & Notes

"""
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(log_content)

    # 4. Initialize Databases
    print("Initializing databases...")
    
    # Memory Database
    conn = sqlite3.connect('data/memory.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS memory_entries (
        id INTEGER PRIMARY KEY,
        content TEXT NOT NULL,
        entry_type TEXT DEFAULT 'fact',
        importance INTEGER DEFAULT 5,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

    # Activity Database
    conn = sqlite3.connect('data/activity.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        source TEXT,
        request TEXT,
        status TEXT DEFAULT 'pending',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        completed_at DATETIME,
        summary TEXT
    )''')
    conn.commit()
    conn.close()

    print("\nSUCCESS: Memory infrastructure initialized! You are ready to go.")

if __name__ == "__main__":
    initialize_environment()
