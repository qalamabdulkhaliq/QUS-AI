# QUS-AI Project Structure

This document outlines the modular architecture of the QUS-AI Islamic Alignment Framework (v2).

```text
QUS-AI/
├── qusai_core/                 # [CORE PACKAGE] Main framework logic
│   ├── __init__.py             # Package definition
│   ├── alignment/              # [MIZAN] Alignment & Safety Logic
│   │   ├── __init__.py
│   │   └── mizan.py            # The 5-point Salat Validation Checkpoints
│   ├── ontology/               # [TAWHID] Knowledge Graph Engine
│   │   ├── __init__.py
│   │   └── engine.py           # RDF loading, traversing, and context lookup
│   ├── llm/                    # [AKL] Model Abstraction Layer
│   │   ├── __init__.py
│   │   └── loader.py           # HuggingFace/Torch loader (CPU/GPU agnostic)
│   ├── pipeline/               # [AMAL] Execution Pipeline
│   │   ├── __init__.py
│   │   └── middleware.py       # Connects Input -> Validator -> Ontology -> Model
│   └── utils/                  # Shared utilities
│       ├── __init__.py
│       └── constants.py        # URI Namespaces (ALIGN, QURAN, ROOT) and Paths
│
├── data/                       # [DATA] Ontologies and Rules
│   ├── quran_root_ontology_v3.ttl   # The main RDF Knowledge Graph
│   └── quranic_grammar_rules.json   # JSON-based grammar logic
│
├── docs/                       # Project Documentation
│   ├── 00_axioms.md
│   ├── README_V2.md
│   └── ...
│
├── qusai_app.py                # [ENTRY] Main Gradio Application Entry Point
├── requirements.txt            # Python dependencies
└── README.md                   # GitHub landing page & HF Metadata
```

## Key Directory Descriptions

- **`qusai_core/`**: This is the heart of the application. It is designed to be portable. You can copy this folder into any other Python project to give it "Quranic Alignment" capabilities.
- **`data/`**: specific data files loaded by `ontology/engine.py`.
- **`qusai_app.py`**: A lightweight wrapper that initializes `qusai_core.pipeline.middleware` and launches the UI.
