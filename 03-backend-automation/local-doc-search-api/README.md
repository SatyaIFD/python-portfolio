# Local Document Search Engine API

An intermediate, locally hosted **FastAPI** microservice that recursively indexes a directory of text files, Markdown files, PDFs, or Word documents (`.docx`). Instead of slow, naive raw string scanning, it converts document corpora into an in-memory keyword bag-of-words matrix, ranking text relevance matches utilizing the **BM25Okapi** scoring algorithm.

---

## 🏗️ Architecture Overview

1. **API Layer (`app/main.py`)**: Uses FastAPI & Pydantic to host structural endpoints and handle payload input parameter compliance.
2. **Indexing Core Engine (`app/core/engine.py`)**: Recursively walks directories, strips texts across various mime-types safely, tokenizes terms via Regular Expressions, and builds an active search index.
3. **GUI Desktop Client (`app/gui/layout.py`)**: A desktop utility enabling physical navigation selection for backend payload processing.

---

## 🚀 Setting Up & Running

### 1. Installation
Ensure you have Python 3.9+ environment configured, then install dependencies:
```bash
pip install -r requirements.txt
pip install -e .