# 📡 RFID-RAG
AI-Powered Retrieval-Augmented Generation System for RFID Knowledge

RFID-RAG is an AI-based question-answering system designed to deliver accurate, contextual, and natural answers for RFID (Radio Frequency Identification) topics.

This project combines semantic vector search, a curated local knowledge base, large language models (LLMs), and an online search fallback to ensure reliable answers even when local knowledge is incomplete.

---

## ✨ Features

- 🔍 Semantic vector search (meaning-based, not keyword-based)
- 🧠 Hybrid RAG architecture (Local KB + Online Search + LLM)
- 🌐 Online search fallback when confidence is low
- 🗂️ Human-in-the-loop knowledge approval system
- 📊 Confidence score for every answer
- 🔌 API-first design (easy integration with web, WhatsApp, Telegram, n8n)
- 💻 Runs on CPU (no GPU required)

---

## 🏗️ System Architecture

User Question
↓
Vector Search (Local Knowledge Base)
↓
Confidence Evaluation
┌──────────────────┐
│ High Confidence │ → Local RAG Answer
└──────────────────┘
┌──────────────────┐
│ Low Confidence │ → Online Search → LLM
└──────────────────┘
↓
(Optional) Save to Pending Knowledge Base


---

## 📁 Project Structure

rfid-rag/
│
├── app.py # FastAPI entry point
├── rag.py # Core RAG engine
├── vectorstore.py # Vector similarity search
├── online_search.py # Online search logic
│
├── data/
│ ├── data.json # Approved knowledge base
│ └── data_pending.json # Pending (online) data
│
├── requirements.txt
└── README.md


---

## ⚙️ Tech Stack

| Layer | Technology |
|-----|-----------|
| API | FastAPI |
| LLM | Mistral (via Ollama) |
| Embeddings | Sentence Transformers |
| Vector Search | Cosine Similarity |
| Search | DuckDuckGo / Custom Search API |
| Storage | JSON Knowledge Base |
| Deployment | CPU-only |

---

## 🚀 Getting Started (Conda Environment)

### 1. Install Conda
Recommended: Miniconda  
https://docs.conda.io/en/latest/miniconda.html

---

### 2. Create Conda Environment

```bash
conda create -n rfid-rag python=3.10 -y
conda activate rfid-rag
```

---

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
### 4. Install & Run Ollama
Install Ollama:
https://ollama.com

Pull LLM model:
```bash
ollama pull mistral
```
Run Ollama server:
```bash
ollama serve
```
Ollama runs at:

```bash
Ollama runs at:
```

### 5. Run the API Server

```bash
uvicorn app:app --reload
```
API will be available at:

```bash
http://localhost:8000
```

## Knowledge Workflow
1. User asks a question
2. System performs semantic vector search
3. If confidence is low:
   - Online search is triggered
   - LLM generates an answer
4. Online answers are saved to:
```bash
data/data_pending.json
```
5. data/data_pending.json
6. Approved knowledge is stored in:
```bash
data/data.json
```
