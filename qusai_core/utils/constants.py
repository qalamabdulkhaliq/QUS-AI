from rdflib import Namespace
from pathlib import Path

# Namespaces
ALIGN = Namespace("http://ontology.alignment/core#")
QURAN = Namespace("http://ontology.quran/")
ROOT = Namespace("http://ontology.quran/root/")
LEMMA = Namespace("http://ontology.quran/lemma/")

# Paths (Assuming relative to the project root, can be overridden)
DEFAULT_ONTOLOGY_PATH = Path("quran_root_ontology_v3.ttl")
DEFAULT_GRAMMAR_PATH = Path("quranic_grammar_rules.json")

# Axioms
SOURCE_NAME = "Allah (الله)"
SHAHADA = "لا إله إلا الله"
NECESSARY_BEING = ALIGN.NecessaryBeing
CONTINGENT_BEING = ALIGN.ContingentBeing
