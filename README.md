# RFID-RAG: Retrieval-Augmented Generation for RFID Data

**Repository:** https://github.com/dindamajesty13/rfid-rag  
**Author:** Dinda Majesty

---

## Overview

This project implements a **Retrieval-Augmented Generation (RAG)** pipeline that integrates large language models (LLMs) with a vector-based retrieval system, specifically designed to work with **RFID data sources**. The goal is to improve the **accuracy and relevance of generated responses** when querying structured RFID traces and associated metadata.

RAG is widely studied in modern NLP for tasks where grounding a model’s output in external knowledge (retrieved documents or traces) can reduce hallucination and improve factuality. This project explores the impact of retrieval quality and retrieval-generation interaction in a real-world IoT dataset context.

---

## Research Scope

This repository is intended as an **exploratory research artifact**, not a production system. 
The focus is on understanding how retrieval mechanisms, confidence estimation, and fallback strategies 
affect the grounding behavior and reliability of large language models when applied to structured, non-textual data.

---

## Motivation

Large language models often produce **plausible but ungrounded answers** when no explicit knowledge is available within model parameters. Combining LLMs with external knowledge sources (via vector retrieval and embeddings) helps anchor responses on **actual data**, addressing:

- hallucination in generative responses  
- domain-specific queries where raw LLM answers are insufficient  
- grounding language generation on structured sensor traces

This repository explores RAG for RFID log data — a non-textual, structured source relevant to logistics and warehouse management.

---

## Features

- Semantic vector retrieval for structured RFID traces
- Hybrid RAG design combining local retrieval and external search
- Confidence-based routing for generation control
- Human-in-the-loop knowledge validation mechanism
- API-based experimental interface for querying and evaluation
- CPU-only deployment for reproducible experimentation

---

## System Architecture

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

## Project Structure

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

## Tech Stack

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

## Retrieval & Generation Pipeline

This project implements a RAG pipeline with the following components:

1. **Document/trace embedding generation**  
   Using embedding models to map RFID traces into vector space.

2. **Vector index creation**  
   Building a FAISS (or similar) index for efficient retrieval.

3. **Query contextualization**  
   Formulating NLP queries that mix natural language and trace context.

4. **Retrieval & fusion**  
   Retrieving relevant traces/documents and fusing into a prompt.

5. **LLM generation**  
   Generating responses from an instruction-tuned or base LLM.

---

## Research Contributions (Exploratory)

This project includes exploratory research on:

- retrieval quality vs. generated response factuality  
- effects of contextualized queries on hallucination control  
- comparison of raw vs. RAG-augmented LLM outputs
- domain-specific vs. generic retrieval strategies
- serves as preliminary groundwork for studying controllable LLM behavior under domain constraints

---

## Getting Started (Conda)

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

## Knowledge Workflow

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

---

## Future Work
Planned extensions include:
1. Quantitative evaluation with relevant datasets
2. Systematic measurement of retrieval accuracy vs. hallucination rate
3. Advanced retrieval fusion techniques (e.g., re-rankers)
