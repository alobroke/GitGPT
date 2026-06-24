# Repository RAG Assistant

An intelligent Retrieval-Augmented Generation (RAG) system that enables developers to ask natural language questions about any GitHub repository and receive context-aware answers grounded in the repository's source code.

---

## Overview

Repository RAG Assistant combines:

* AST-based code chunking
* Semantic embeddings
* FAISS vector search
* Cross-Encoder reranking
* Large Language Models (Qwen 2.5 Coder)

to create an AI-powered code understanding system capable of answering repository-specific questions.

Instead of manually searching through hundreds of files, developers can ask:

* How does OAuth authentication work?
* What does `make_not_authenticated_error()` do?
* How are security scopes handled?
* Which files are involved in user authentication?

and receive answers grounded in the repository source code.

---

## Features

### Intelligent Code Chunking

* AST-based Python parsing
* Function-level chunking
* Method-level chunking
* Class metadata extraction
* Duplicate reduction

### Semantic Search

* BAAI BGE embeddings
* FAISS vector indexing
* Similarity search
* Fast retrieval

### Reranking

* Cross-Encoder reranking
* Improved retrieval quality
* Better repository grounding

### LLM-Powered Answers

* Qwen2.5-Coder integration
* Context-aware code explanations
* Repository-focused responses
* Source-backed answers

### REST API

* FastAPI backend
* Swagger documentation
* JSON request/response format

---

## Architecture

```text
GitHub Repository
        │
        ▼
AST Code Chunking
        │
        ▼
Code Chunks
        │
        ▼
BGE Embeddings
        │
        ▼
FAISS Vector Store
        │
        ▼
Retriever
        │
        ▼
Cross Encoder Reranker
        │
        ▼
Qwen2.5-Coder
        │
        ▼
Generated Answer
```

---

## Tech Stack

### Backend

* Python
* FastAPI
* Pydantic

### Retrieval

* FAISS
* Sentence Transformers

### Embeddings

* BAAI/bge-small-en-v1.5

### Reranking

* cross-encoder/ms-marco-MiniLM-L-6-v2

### LLM

* Qwen/Qwen2.5-Coder-3B-Instruct

---

## Project Structure

```text
backend/
│
├── api/
│   ├── routes.py
│   └── schemas.py
│
├── embeddings/
│   ├── embedder.py
│   └── build_index.py
│
├── ingestion/
│   ├── chunker.py
│   └── build_chunks.py
│
├── llm/
│   ├── model_loader.py
│   ├── generator.py
│   └── prompt.py
│
├── rag/
│   └── pipeline.py
│
├── retrieval/
│   ├── retriever.py
│   └── reranker.py
│
└── main.py

tests/
data/
docs/
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd repository-rag-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Build Knowledge Base

### Step 1: Generate Chunks

```bash
python -m backend.ingestion.build_chunks
```

### Step 2: Generate Embeddings

```bash
python -m backend.embeddings.build_index
```

---

## Start API Server

```bash
uvicorn backend.main:app
```

Server:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

## Example API Request

### POST /ask

Request:

```json
{
  "question": "What does make_not_authenticated_error do?"
}
```

Response:

```json
{
  "answer": "The make_not_authenticated_error method creates an HTTPException with status code 401 and sets the WWW-Authenticate header..."
}
```

---

## Example Questions

* How does OAuth authentication work?
* What is the purpose of Security()?
* How are OAuth scopes handled?
* Explain the authentication flow.
* Which files implement API key security?
* How does dependency injection work?

---

## Performance

Current pipeline:

* AST-based chunking
* 588 indexed chunks
* FAISS vector retrieval
* Cross-Encoder reranking
* Qwen 2.5 Coder generation

---

## Future Roadmap

* Multi-language repository support
* Multi-repository indexing
* Hybrid Search (BM25 + Vector Search)
* Docker deployment
* React frontend
* Conversation memory
* GitHub repository ingestion via URL
* Source citations in responses
* GitHub Action integration

---

## License

MIT License

---


