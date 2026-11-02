# SpecTower

**An AI-powered research assistant for 3GPP LTE and 5G technical specifications.**

SpecTower helps telecom protocol engineers find relevant requirements in lengthy 3GPP specifications by asking questions in plain English. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant specification clauses while preserving clause numbers, specification versions, and release information.

## Problem Statement

Telecom protocol test engineers often spend hours searching through thousands of pages of 3GPP technical specifications to identify exact protocol requirements.

Finding the correct clause across different specification versions and releases can be time-consuming.

SpecTower aims to simplify this process by enabling engineers to ask natural-language questions and retrieve relevant technical clauses with source references.

## Who Is It For?

- Telecom protocol test engineers working with LTE and 5G standards.
- Telecom engineering teams supporting operator and chipset clients.

## Key Features

- **Document ingestion:** Process 3GPP technical specification documents.
- **Clause-aware extraction:** Extract structured sections while preserving clause numbers.
- **Metadata preservation:** Store specification numbers, versions, and releases.
- **Semantic retrieval:** Retrieve relevant clauses using vector embeddings.
- **Source traceability:** Return the original specification and clause information with retrieved content.

## Technology Stack

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Document processing | python-docx |
| Vector database | ChromaDB |
| Embeddings | ChromaDB embedding function |
| API validation | Pydantic |
| Code quality | Ruff, Pytest |

## Dataset

SpecTower uses official 3GPP technical specifications.

| Specification series | Focus |
|---|---|
| Series 23 | System architecture |
| Series 24 | Signalling |
| Series 36 | LTE radio |
| Series 38 | 5G NR |

**Current sample dataset:**
- TS 23.501
- TS 24.501
- TS 38.331
- Additional document parts from TS 24.501

Official source: [3GPP Specifications](https://www.3gpp.org/specifications)

The long-term dataset target is 25,000+ pages across several hundred specifications. This is a target, not the current indexed dataset.

## RAG Pipeline

```text
3GPP Specification Documents
          |
          v
     DOCX Extraction
          |
          v
   Clause Identification
          |
          v
   Metadata Preservation
          |
          v
    Structured JSONL
          |
          v
   Text Embeddings
          |
          v
       ChromaDB
          |
          v
    Semantic Retrieval
          |
          v
   Relevant Clauses
```

## Current Progress

- [x] Selected official 3GPP specifications.
- [x] Downloaded sample specification documents.
- [x] Implemented DOCX text extraction.
- [x] Preserved clause numbers and specification metadata.
- [x] Extracted 2,552 sections from 8 DOCX documents.
- [x] Generated structured JSONL output.
- [x] Integrated ChromaDB with FastAPI.
- [x] Implemented batch-based indexing.
- [x] Implemented a semantic retrieval API.
- [ ] Complete and validate full dataset indexing.
- [ ] Evaluate retrieval quality using real telecom questions.
- [ ] Generate evidence-backed natural-language answers.
- [ ] Add clause-level citations and answer verification.
- [ ] Implement resumable ingestion with Redis workers and checkpoints.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ranjithavenkadesan06-hue/SpecTower.git
cd SpecTower
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure environment variables

```powershell
copy .env.example .env
```

### 6. Start the FastAPI server

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application health |
| POST | `/index` | Index extracted specification clauses |
| POST | `/query` | Retrieve relevant specification clauses |

### Example query

```json
{
  "question": "What does the 5G system architecture define?",
  "spec_number": "23.501"
}
```

The query endpoint returns relevant clauses with specification metadata and retrieval distances.

**Note:** The current implementation performs semantic retrieval. LLM-generated answers and final citation verification are planned improvements.

## Key Engineering Challenges

### 1. Large-scale document ingestion

Processing thousands of pages requires reliable extraction and structured storage. Future improvements include resumable background workers, checkpoints, and retry handling.

### 2. Clause and version preservation

Technical answers must refer to the correct specification and release. SpecTower preserves specification numbers, versions, releases, and clause identifiers as metadata.

### 3. Retrieval accuracy

Relevant clauses must be retrieved even when engineers use natural language rather than exact technical terminology. Retrieval evaluation and improved chunking are planned.

## Future Improvements

- Redis-backed resumable ingestion workers.
- Checkpointing and automatic retry handling.
- Improved clause-aware chunking.
- Advanced retrieval and reranking.
- LLM-powered answer generation.
- Evidence verification and clause citations.
- Ingestion progress monitoring.

## Project Goal

Build a reliable AI research assistant that helps telecom engineers navigate complex LTE and 5G standards, retrieve exact technical requirements, and verify answers against original 3GPP specifications.