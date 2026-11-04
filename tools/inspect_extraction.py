import json
from collections import Counter
from pathlib import Path

path = Path("data/processed/clauses.jsonl")

records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]

print("TOTAL RECORDS:", len(records))

print("\nRECORD COUNTS BY FILE")
counts = Counter(Path(r["source_file"]).name for r in records)

for filename, count in counts.items():
    print(f"{filename}: {count}")

print("\nSAMPLE RECORDS")

for record in records[:20]:
    print("-" * 60)
    print("Spec:", record["spec_number"])
    print("Version:", record["version"])
    print("Release:", record["release"])
    print("Clause:", record["clause"])
    print("Title:", record["title"])
    print("Parent:", record["parent_heading"])
    print("Content:", record["content"][:250])

print("\nMETADATA CHECK")

for field in ["spec_number", "version", "release"]:
    missing = sum(r[field] is None for r in records)
    print(f"{field}: {missing} missing")
