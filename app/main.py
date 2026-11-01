import json
from functools import lru_cache
from pathlib import Path

import chromadb
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel

from app.config import Settings, get_settings

app = FastAPI(title="SpecTower", version="1.0.0")

SettingsDep = Depends(get_settings)

DATA_PATH = Path("data/processed/clauses.jsonl")
DB_PATH = Path("data/chroma_db")


@lru_cache
def get_collection():
    print("Connecting to ChromaDB...", flush=True)

    client = chromadb.PersistentClient(path=str(DB_PATH))

    collection = client.get_or_create_collection(
        name="spectower_clauses",
        metadata={"hnsw:space": "cosine"}
    )

    print("ChromaDB collection loaded", flush=True)
    return collection


class QueryRequest(BaseModel):
    question: str
    spec_number: str | None = None


@app.get("/health")
def health(settings: Settings = SettingsDep):
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment
    }


@app.post("/index")
def index_documents():
    print("Starting document indexing...", flush=True)

    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail="Clauses file not found"
        )

    collection = get_collection()

    batch_size = 100
    indexed = 0

    ids = []
    documents = []
    metadatas = []

    with DATA_PATH.open("r", encoding="utf-8") as file:

        for i, line in enumerate(file):

            record = json.loads(line)
            content = record.get("content", "").strip()
            if not content:
                continue
            content = content[:3000]
            ids.append(f"clause_{i}")

            documents.append(
                f"TS {record['spec_number']} "
                f"Clause {record['clause']}: "
                f"{record['title']}\n{content}"
            )


            metadatas.append({
                "spec_number": record["spec_number"],
                "version": record["version"],
                "release": record["release"],
                "clause": record["clause"],
                "title": record["title"],
                "source_file": record["source_file"]
            })

            if len(ids) == batch_size:

                print(
                    f"Starting batch of {len(ids)} clauses...",
                    flush=True
                )

                collection.upsert(
                    ids=ids,
                    documents=documents,
                    metadatas=metadatas
                )

                indexed += len(ids)

                print(
                    f"Successfully indexed {indexed} clauses",
                    flush=True
                )

                ids, documents, metadatas = [], [], []

    # Process remaining clauses
    if ids:

        print(
            f"Starting final batch of {len(ids)} clauses...",
            flush=True
        )

        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas
        )

        indexed += len(ids)

    print("Indexing completed!", flush=True)

    return {
        "message": "Indexing completed",
        "indexed_clauses": indexed,
        "total_in_database": collection.count()
    }


@app.post("/query")
def query_documents(request: QueryRequest):

    collection = get_collection()

    total = collection.count()

    if total == 0:
        raise HTTPException(
            status_code=400,
            detail="No documents indexed. Call POST /index first."
        )

    filters = None

    if request.spec_number:
        filters = {"spec_number": request.spec_number}

    results = collection.query(
        query_texts=[request.question],
        n_results=min(5, total),
        where=filters,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    matches = []

    for document, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0],
    strict=False
   ):

        matches.append({
            "content": document,
            "spec_number": metadata["spec_number"],
            "version": metadata["version"],
            "release": metadata["release"],
            "clause": metadata["clause"],
            "title": metadata["title"],
            "distance": distance
        })

    return {
        "question": request.question,
        "retrieved_clauses": matches
    }
