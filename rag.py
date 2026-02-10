import json
import faiss
import requests
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer
from online_search import online_search
from services.ingestion import submit_contribution

# =========================
# CONFIG
# =========================
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

LLM_MODEL = "mistral"
OLLAMA_URL = "http://localhost:11434/api/generate"

TOP_K = 3
RAG_THRESHOLD = 0.55
ONLINE_FALLBACK_THRESHOLD = 0.45
MIN_CONFIDENCE = 0.3
MAX_CONFIDENCE = 0.95


# =========================
# DATASET
# =========================
def load_dataset(path: str) -> List[Dict]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [item for item in data if item.get("status") == "approved"]


def build_corpus(data: List[Dict]):
    corpus = []
    metadata = []

    for item in data:
        q = item.get("question", "").strip()
        a = item.get("answer", "").strip()

        if not q or not a:
            continue

        text = f"Pertanyaan: {q}\nJawaban: {a}"

        corpus.append(text)
        metadata.append({
            "id": item.get("id"),
            "question": q,
            "answer": a,
            "category": item.get("category"),
        })

    if not corpus:
        raise RuntimeError("Corpus kosong")

    return corpus, metadata


# =========================
# VECTOR STORE (COSINE)
# =========================
class VectorStore:
    def __init__(self, texts: List[str]):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=True
        ).astype("float32")

        faiss.normalize_L2(embeddings)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def search(self, query: str, k: int):
        query_emb = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype("float32")

        faiss.normalize_L2(query_emb)
        scores, indices = self.index.search(query_emb, k)

        return scores[0], indices[0]


# =========================
# LLM (OLLAMA)
# =========================
def call_llm(prompt: str) -> str:
    payload = {
        "model": LLM_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.6,
            "top_p": 0.9,
            "repeat_penalty": 1.1
        }
    }

    try:
        res = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=3000
        )
        res.raise_for_status()
        return res.json()["response"].strip()

    except requests.exceptions.ReadTimeout:
        return (
            "Maaf, sistem sedang memproses jawaban lebih lama dari biasanya. "
            "Silakan coba ulangi pertanyaan sebentar lagi."
        )

    except Exception as e:
        return f"Terjadi kesalahan sistem: {str(e)}"

def build_online_prompt(question: str, context: str) -> str:
        return f"""
    Kamu adalah asisten teknis RFID yang menjelaskan dengan bahasa Indonesia
    yang alami, ringkas, dan mudah dipahami.

    Gunakan informasi berikut sebagai referensi umum:
    {context}

    Pertanyaan:
    {question}

    Jawaban:
    """.strip()

# =========================
# RAG ENGINE
# =========================
class RAGEngine:
    def __init__(self, dataset_path: str):
        self.dataset_path = dataset_path
        self.reload()

    def reload(self):
        self.data = load_dataset(self.dataset_path)
        self.corpus, self.metadata = build_corpus(self.data)
        self.vstore = VectorStore(self.corpus)
        print(f"RAG loaded: {len(self.corpus)} knowledge")

    def _confidence(self, score: float, pure_llm=False) -> float:
        if pure_llm:
            return 0.85
        return round(max(MIN_CONFIDENCE, min(MAX_CONFIDENCE, score)), 2)

    def _build_context(self, indices: List[int]) -> str:
        return "\n\n".join(
            f"Q: {self.metadata[i]['question']}\nA: {self.metadata[i]['answer']}"
            for i in indices
        )


    def _prompt(self, question: str, context: str = "") -> str:
        return f"""
    Kamu adalah asisten ahli RFID dan sistem komunikasi radio.
    Jawab dengan bahasa Indonesia yang natural, jelas, dan profesional.

    Aturan:
    - Jangan terdengar seperti buku teks
    - Jangan menyebut kata "konteks" atau "data di atas"
    - Jika topik umum, jelaskan dari dasar
    - Jika teknis, jelaskan bertahap

    Referensi (jika relevan):
    {context}

    Pertanyaan:
    {question}

    Jawaban:
    """.strip()

    def ask(self, question: str, use_llm: bool = True):
        scores, indices = self.vstore.search(question, TOP_K)
        best_score = float(scores[0])

        # ===== CASE 1: RAG LOKAL =====
        if best_score >= ONLINE_FALLBACK_THRESHOLD:
            context = self._build_context(indices)
            sources = [self.metadata[i].get("id", "unknown") for i in indices]

            if not use_llm:
                idx = int(indices[0])
                return {
                    "answer": self.metadata[idx]["answer"],
                    "confidence": self._confidence(best_score),
                    "sources": sources,
                    "mode": "rag"
                }

            prompt = self._prompt(question, context)
            answer = call_llm(prompt)

            return {
                "answer": answer,
                "confidence": self._confidence(best_score),
                "sources": sources,
                "mode": "rag"
            }

        # ===== CASE 2: ONLINE SEARCH =====
        online = online_search(question)

        if online["answer"].strip():
            prompt = self._prompt(question, online["answer"])
            answer = call_llm(prompt)

            submit_contribution({
                "question": question,
                "answer": answer,
                "source": "online-search",
                "confidence": 0.6,
                "references": online["sources"]
            })

            return {
                "answer": answer,
                "confidence": 0.6,
                "sources": [
                    s.get("url") for s in online["sources"]
                ],
                "mode": "online"
            }

        # ===== CASE 3: PURE LLM =====
        prompt = self._prompt(question)
        answer = call_llm(prompt)

        return {
            "answer": answer,
            "confidence": 0.85,
            "sources": ["llm-generated"],
            "mode": "llm"
        }

# =========================
# CLI TEST
# =========================
if __name__ == "__main__":
    rag = RAGEngine("dataset.json")

    while True:
        q = input("\nPertanyaan: ")
        if q.lower() in ["exit", "quit"]:
            break

        res = rag.ask(q, use_llm=True)
        print("\nJawaban:")
        print(res["answer"])
        print("Confidence:", res["confidence"])
        print("Sources:", res["sources"])
