# SpecTower

## Problem

Telecom protocol test engineers spend hours searching thousands of pages of 3GPP specifications to find exact requirements for LTE and 5G protocols. Different teams work with different specification releases, making it difficult to find accurate, version-specific answers. SpecTower allows engineers to ask questions in plain English and receive answers backed by relevant specification clauses and citations. It aims to make telecom standards research faster, more reliable, and easier to verify.

## Who it is for

- Telecom protocol test engineers working with LTE and 5G standards.
- Telecom engineering teams supporting operator and chipset clients.

## Signature feature

Clause-aware RAG with a research agent that retrieves relevant specification clauses, generates evidence-backed answers, and verifies claims against source documents.

## Hardest problem (my interview story)

The main challenge is processing thousands of pages of technical specifications reliably. SpecTower aims to use Redis-backed workers, checkpoints, and retry handling to resume interrupted ingestion without reprocessing completed files or creating duplicate chunks. Another challenge is preserving specification versions and clause numbers so that answers reference the correct technical requirements.

## Dataset

| **Source** | **Link** | **Documents** | **Pages** | **Licence / terms** |
| ---------- | -------- | ------------- | --------- | ------------------- |
| 3GPP technical specifications (Series 23, 24, 36, and 38) | [Official 3GPP Specifications](https://www.3gpp.org/specifications) | Several hundred (target) | 25,000+ (target) | Check applicable 3GPP terms and notices |

## 10 real questions

See [docs/QUESTIONS.md](https://github.com/govindchandak/genai-starter-repo/blob/main/docs/QUESTIONS.md).

## Run it

```bash
python -m venv .venv
```

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
```

```bash
pip install -r requirements-dev.txt
```

```powershell
# Windows
copy .env.example .env
```

```bash
uvicorn app.main:app --reload
```

Health check: `http://localhost:8000/health`

## Live link



Added in Week 2.

# SpecTower

SpecTower is a project I'm building to make it easier to find information in 3GPP LTE and 5G technical specifications.

These documents can be long, and finding the exact clause related to a protocol question can take time. The idea is to let users ask questions in plain English and get answers based on the relevant specification, with references to the source clauses.

## What I'm working on

- Collecting official 3GPP specifications related to LTE and 5G.
- Extracting text and keeping the clause numbers and document versions.
- Finding relevant sections based on a user's question.
- Generating answers with references to the original specifications.

## Dataset

I'm starting with **TS 38.331 — NR; Radio Resource Control (RRC); Protocol specification**.

Source: [Official 3GPP specifications](https://www.3gpp.org/specifications)

The initial document has been downloaded. Text extraction and search functionality are the next steps.

## Planned technology

- Python
- FastAPI
- Embeddings and a vector database
- Retrieval-Augmented Generation (RAG)

## Current progress

- [x] Selected an initial 3GPP specification
- [x] Downloaded the specification archive
- [ ] Extract text from the document
- [ ] Preserve clause numbers and version details
- [ ] Implement semantic search
- [ ] Generate answers with source references

## Goal

Build a tool that helps telecom engineers find relevant information in 3GPP specifications without having to search through long documents manually.