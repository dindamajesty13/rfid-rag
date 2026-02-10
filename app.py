from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.ingestion import (
    submit_contribution,
    approve_contribution,
    reject_contribution,
)
from services import reindex
from services.ingestion import get_pending

DATASET_PATH = "data/data.json"

app = FastAPI(title="RFID RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================
# INIT RAG ON STARTUP
# ======================
@app.on_event("startup")
def startup():
    reindex.init_rag(DATASET_PATH)

# ======================
# SCHEMAS
# ======================
class AskRequest(BaseModel):
    question: str
    use_llm: bool = False

class ContributionRequest(BaseModel):
    title: str
    question: str
    answer: str
    category: str
    difficulty: str
    tags: list[str]
    author: str
    source: str = "user"
    domain: str = "rfid"
    type: str = "qna"
    language: str = "id"

# ======================
# CHAT ENDPOINT
# ======================
@app.post("/ask")
def ask(req: AskRequest):
    if reindex.rag_engine is None:
        raise HTTPException(500, "RAG not ready")

    return reindex.rag_engine.ask(req.question, req.use_llm)

# ======================
# CONTRIBUTE
# ======================
@app.post("/contribute")
def contribute(req: ContributionRequest):
    contribution_id = submit_contribution(req.dict())
    return {
        "message": "Kontribusi berhasil dikirim dan menunggu review",
        "id": contribution_id
    }

# ======================
# ADMIN
# ======================
@app.post("/contributions/{cid}/approve")
def approve(cid: str):
    try:
        approve_contribution(cid)
        reindex.reindex(DATASET_PATH)
        return {"message": "Approved & reindexed"}
    except ValueError:
        raise HTTPException(404, "Contribution not found")

@app.post("/contributions/{cid}/reject")
def reject(cid: str):
    reject_contribution(cid)
    return {"message": "Rejected"}

@app.get("/contributions")
def list_contributions(status: str = "pending"):
    if status != "pending":
        return {"count": 0, "data": []}

    pending = get_pending()

    normalized = [
        {
            "id": x["id"],
            "title": x["title"],
            "question": x["question"],
            "answer": x["answer"],
            "category": x["category"],
            "difficulty": x["difficulty"],
            "authorName": x.get("author", "Anonim"),
            "submittedAt": x["created_at"]
        }
        for x in pending
    ]

    return normalized
