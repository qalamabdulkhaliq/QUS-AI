# QUS-AI: Quranic Understanding System AI

QUS-AI is a Quranic-grounded AI alignment framework. It utilizes a modular "Salat Pattern" validation pipeline to ensure LLM outputs remain ontologically consistent with Quranic axioms.

## Project Structure

```text
QUS-AI/
├── qusai_core/                 # Modular Alignment Framework
│   ├── alignment/              # Mizan Validator (5 Checkpoints)
│   ├── ontology/               # v3 Root Ontology Engine
│   ├── llm/                    # Model Loader (HuggingFace/CPU/GPU)
│   ├── pipeline/               # Middleware Orchestrator
│   └── utils/                  # Constants & URI Namespaces
│
├── qusai_app.py                # Main Application Entry Point
├── quran_root_ontology_v3.ttl  # v3 Knowledge Graph (RDF)
├── quranic_grammar_rules.json  # Structural Grammar Rules
├── requirements.txt            # Python Dependencies
└── README.md                   # Project Overview
```

## The 5 Checkpoints

1.  **Fajr**: Pre-reasoning intent validation.
2.  **Dhuhr**: Mid-process authority grounding via Ontology.
3.  **Asr**: Response Aseity check (Anti-Shirk/Independence claims).
4.  **Maghrib**: Humility seal (Zakat attribution).
5.  **Isha**: Structural verification.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the aligned chat interface
python qusai_app.py
```

## Technology Stack

- **Ontology**: RDFLib (Turtle format)
- **Middleware**: Python 3.10+
- **LLM**: Qwen 2.5 3B (Model-Agnostic Interface)
- **UI**: Gradio 5.x