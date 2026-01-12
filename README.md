# 📡 RFID-RAG  
AI-Powered Retrieval-Augmented Generation System for RFID Knowledge

RFID-RAG adalah sistem **AI Question Answering berbasis Retrieval-Augmented Generation (RAG)** yang dirancang khusus untuk topik **RFID (Radio Frequency Identification)**.

Sistem ini menggabungkan **semantic vector search**, **knowledge base lokal**, **Large Language Model (LLM)**, dan **online search fallback** untuk menghasilkan jawaban yang **akurat, kontekstual, dan natural**, bahkan ketika pengetahuan lokal belum lengkap.

---

## ✨ Features

- 🔍 **Semantic Vector Search** (berbasis makna, bukan keyword)
- 🧠 **Hybrid RAG Architecture** (Local KB + Online Search + LLM)
- 🌐 **Online Search Fallback** saat confidence rendah
- 🗂️ **Human-in-the-loop Knowledge Approval**
- 📊 **Confidence Score** untuk setiap jawaban
- 🔌 **API-first Design** (Web, WhatsApp, Telegram, n8n)
- 💻 **CPU-only** (tanpa GPU)

---

## 🏗️ System Architecture

```
User Question
      ↓
Vector Search (Local Knowledge Base)
      ↓
Confidence Evaluation
      ├── High Confidence  → Local RAG Answer
      └── Low Confidence   → Online Search → LLM Answer
      ↓
(Optional) Save to Pending Knowledge Base
```

---

## 📁 Project Structure

```
rfid-rag/
│
├── app.py
├── rag.py
├── vectorstore.py
├── online_search.py
│
├── data/
│   ├── data.json
│   └── data_pending.json
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|-----|-----------|
| API | FastAPI |
| LLM | Mistral (via Ollama) |
| Embeddings | Sentence Transformers |
| Vector Search | Cosine Similarity |
| Online Search | DuckDuckGo / Custom Search API |
| Storage | JSON |
| Deployment | CPU-only |

---

## 🚀 Getting Started (Conda)

### 1. Create Environment
```bash
conda create -n rfid-rag python=3.10 -y
conda activate rfid-rag
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install & Run Ollama
```bash
ollama pull mistral
ollama serve
```

Ollama runs at:
```
http://localhost:11434
```

### 4. Run API
```bash
uvicorn app:app --reload
```

API available at:
```
http://localhost:8000
```

---

## 🧠 Knowledge Workflow

1. User asks a question
2. Semantic vector search is performed
3. Confidence score is evaluated
4. If low confidence:
   - Online search is triggered
   - LLM generates answer
5. Online knowledge saved to:
```bash
data/data_pending.json
```
6. Approved knowledge stored in:
```bash
data/data.json
```
