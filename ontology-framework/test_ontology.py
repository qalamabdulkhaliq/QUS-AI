import rdflib
from pathlib import Path

BASE_DIR = Path("C:/AlignmentProject")
ontology_file = BASE_DIR / "quran_complete_ontology_v2.ttl"

print(f"File exists: {ontology_file.exists()}")
print(f"File path: {ontology_file}")

if ontology_file.exists():
    size_mb = ontology_file.stat().st_size / 1e6
    print(f"File size: {size_mb:.2f} MB")
    
    with open(ontology_file, 'r', encoding='utf-8') as f:
        first_lines = [f.readline() for _ in range(10)]
        print("\nFirst 10 lines:")
        for i, line in enumerate(first_lines, 1):
            print(f"{i}: {line.strip()}")

graph = rdflib.Graph()
print("\nAttempting to parse...")
try:
    graph.parse(str(ontology_file), format="turtle")
    print(f"✓ SUCCESS: Loaded {len(graph)} triples")
    
    # Show sample triples
    sample = list(graph.triples((None, None, None)))[:3]
    print("\nSample triples:")
    for s, p, o in sample:
        print(f"  {s} -> {p} -> {o}")
except Exception as e:
    print(f"✗ PARSE ERROR: {e}")
    import traceback
    traceback.print_exc()