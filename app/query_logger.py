import datetime
import json

LOG_FILE = "query_log.jsonl"

def log_query(query, answer, reasoning):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "query": query,
        "answer": answer,
        "reasoning": reasoning
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n") 