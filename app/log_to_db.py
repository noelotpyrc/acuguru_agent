import sqlite3
import json

DB_FILE = "query_log.db"
JSONL_FILE = "query_log.jsonl"

# Connect to SQLite database (creates file if not exists)
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''
CREATE TABLE IF NOT EXISTS query_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    query TEXT,
    answer TEXT,
    reasoning TEXT
)
''')

# Read JSONL and insert into DB
with open(JSONL_FILE, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        entry = json.loads(line)
        c.execute(
            "INSERT INTO query_logs (timestamp, query, answer, reasoning) VALUES (?, ?, ?, ?)",
            (entry["timestamp"], entry["query"], entry["answer"], entry["reasoning"])
        )

conn.commit()
conn.close()
print(f"Imported log entries from {JSONL_FILE} to {DB_FILE}") 