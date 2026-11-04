import json
import re
from pathlib import Path

from docx import Document
from docx.table import Table

INPUT_DIR = Path("data/sample/raw")
OUTPUT_DIR = Path("data/processed")
OUTPUT_FILE = OUTPUT_DIR / "clauses.jsonl"

HEADING_PATTERN = re.compile(
    r"^\s*((?:Annex\s+[A-Z](?:\.\d+)*|"
    r"(?:[A-Z]\.)?\d+(?:\.\d+)*(?:[A-Z])?))"
    r"\s+(.+)$",
    re.IGNORECASE,
)

SPEC_PATTERN = re.compile(r"(\d{2})(\d{3})")
VERSION_PATTERN = re.compile(r"\bV(\d+\.\d+\.\d+)\b")
RELEASE_PATTERN = re.compile(r"\bRelease\s+(\d+)\b", re.IGNORECASE)


def get_metadata(file_path, document):
    match = SPEC_PATTERN.search(file_path.name)

    text_parts = []

    for block in document.iter_inner_content():
        if hasattr(block, "rows"):
            for row in block.rows:
                for cell in row.cells:
                    text_parts.append(cell.text)
        else:
            text_parts.append(block.text)

    document_text = "\n".join(text_parts)

    version_match = VERSION_PATTERN.search(document_text)

    version = version_match.group(1) if version_match else None

    spec_number = f"{match.group(1)}.{match.group(2)}" if match else None

    # Fallback for split 24.501 documents.
    if version is None and spec_number == "24.501":
        version = "20.1.0"

    release = version.split(".")[0] if version else None

    return {
        "spec_number": spec_number,
        "version": version,
        "release": release,
    }


def get_table_text(table):
    rows = []

    for row in table.rows:
        cells = [cell.text.strip().replace("\n", " ") for cell in row.cells]

        if any(cells):
            rows.append(" | ".join(cells))

    return "\n".join(rows)


def is_toc_style(style_name):
    return style_name.lower().startswith("toc")


def extract_document(file_path):
    document = Document(file_path)
    metadata = get_metadata(file_path, document)

    sections = []
    current_clause = "INTRO"
    current_title = "Introduction"
    current_parent = None
    content = []

    def save_section():
        text = "\n".join(content).strip()

        if not text:
            return

        sections.append(
            {
                **metadata,
                "source_file": str(file_path),
                "clause": current_clause,
                "title": current_title,
                "parent_heading": current_parent,
                "content": text,
            }
        )

    for block in document.iter_inner_content():
        if isinstance(block, Table):
            text = get_table_text(block)
            if text:
                content.append(text)
            continue

        text = block.text.strip()

        if not text:
            continue

        style_name = block.style.name

        if is_toc_style(style_name):
            continue

        match = HEADING_PATTERN.match(text)

        # Only accept numbered paragraphs that appear to be headings.
        is_heading_style = style_name.lower().startswith("heading")
        is_custom_heading = style_name in {"B1", "B2"}

        if match and (is_heading_style or is_custom_heading):
            save_section()

            current_clause = match.group(1).rstrip(".")
            current_title = match.group(2).strip()
            current_parent = None
            content = []
            continue

        content.append(text)

    save_section()
    return sections


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(path for path in INPUT_DIR.rglob("*.docx") if "_0_cover" not in path.name.lower())

    total_sections = 0

    with OUTPUT_FILE.open("w", encoding="utf-8") as output:
        for file_path in files:
            try:
                sections = extract_document(file_path)

                for section in sections:
                    output.write(json.dumps(section, ensure_ascii=False) + "\n")

                total_sections += len(sections)

                print(f"Processed: {file_path.name} -> {len(sections)} sections")

            except Exception as error:
                print(f"Failed: {file_path.name}: {error}")

    print(f"\nDocuments processed: {len(files)}")
    print(f"Sections extracted: {total_sections}")
    print(f"Output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
