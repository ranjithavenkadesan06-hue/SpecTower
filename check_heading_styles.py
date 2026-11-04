from collections import Counter
from pathlib import Path

from docx import Document

INPUT_DIR = Path("data/sample/raw")

for file_path in sorted(INPUT_DIR.rglob("*.docx")):
    document = Document(file_path)

    styles = Counter(paragraph.style.name for paragraph in document.paragraphs if paragraph.text.strip())

    print(f"\n--- {file_path.name} ---")

    for style, count in styles.most_common():
        print(f"{style}: {count}")
