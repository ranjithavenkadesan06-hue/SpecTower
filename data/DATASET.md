@'
# SpecTower Dataset

## Purpose

SpecTower is a retrieval-augmented generation (RAG) project for searching
5G and LTE standards and returning relevant clauses with source references.

## Sources

Official 3GPP specifications and archive directories:

- https://www.3gpp.org/specifications
- https://www.3gpp.org/ftp/Specs/archive/23_series/23.501/
- https://www.3gpp.org/ftp/Specs/archive/38_series/38.331/

## Current local sample documents

| File | Specification | Version | Release | Document date |
|---|---|---|---|---|
| 23501-k30.docx | 3GPP TS 23.501 - System architecture for the 5G System (5GS); Stage 2 | V20.3.0 | 20 | 2026-09 |
| 38331-j40.docx | 3GPP TS 38.331 - NR; Radio Resource Control (RRC) protocol specification | V19.4.0 | 19 | 2026-09 |

## Integrity and tracking

File sizes and SHA256 checksums are recorded in `data/manifest.csv`.
Source URLs currently point to archive directories; exact file-level download
URLs and actual download dates have not yet been verified.

## Data handling

The full DOCX files are kept locally under `data/sample/raw/` and are ignored
by Git. Do not redistribute the documents or commit them to the repository
unless the applicable 3GPP terms and permissions have been checked.

## Current scope and limitations

- Two DOCX documents have been collected.
- The total page count has not yet been measured.
- The collection is not yet a complete 5G/LTE standards corpus.
- Document versions and releases should be preserved during ingestion and retrieval.
'@ | Set-Content data/DATASET.md -Encoding utf8