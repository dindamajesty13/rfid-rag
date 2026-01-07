import json
from datetime import datetime
from pathlib import Path
import os
import uuid

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

APPROVED_FILE = DATA_DIR / "data.json"
PENDING_FILE = DATA_DIR / "data_pending.json"

def load_json(path, default=None):
    if default is None:
        default = []

    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return default

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def submit_contribution(payload: dict):
    pending = load_json(PENDING_FILE)
    now = datetime.utcnow().isoformat() + "Z"

    item = {
        "id": f"pending-{uuid.uuid4().hex[:8]}",
        "title": payload.get("title") or payload["question"][:60],
        "question": payload["question"],
        "answer": payload["answer"],
        "category": payload.get("category", "Umum"),
        "difficulty": payload.get("difficulty", "Basic"),
        "tags": payload.get("tags", []),
        "author": payload.get("author", "System"),
        "source": payload.get("source", "unknown"),
        "domain": payload.get("domain", "general"),
        "type": payload.get("type", "qna"),
        "language": payload.get("language", "id"),
        "status": "pending",
        "confidence": payload.get("confidence", 0.6),
        "created_at": now,
        "updated_at": now,
        "content": f"Pertanyaan: {payload['question']}\nJawaban: {payload['answer']}"
    }

    pending.append(item)
    save_json(PENDING_FILE, pending)

    return item["id"]

def get_pending():
    return load_json(PENDING_FILE)

def approve_contribution(contribution_id: str):
    pending = load_json(PENDING_FILE)
    approved = load_json(APPROVED_FILE)

    item = next((x for x in pending if x["id"] == contribution_id), None)
    if not item:
        raise ValueError("Contribution not found")

    pending = [x for x in pending if x["id"] != contribution_id]

    item["id"] = f"rfid-{len(approved)+1:06d}"
    item["status"] = "approved"
    item["updated_at"] = datetime.utcnow().isoformat() + "Z"

    # fallback content
    if not item.get("content"):
        item["content"] = item["answer"]

    approved.append(item)

    save_json(PENDING_FILE, pending)
    save_json(APPROVED_FILE, approved)

    return item

def reject_contribution(contribution_id: str):
    pending = load_json(PENDING_FILE)
    pending = [x for x in pending if x["id"] != contribution_id]
    save_json(PENDING_FILE, pending)
