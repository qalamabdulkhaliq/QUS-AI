---
title: QUS-AI Mizan
emoji: 🕌
colorFrom: green
colorTo: blue
sdk: gradio
sdk_version: 5.9.1
python_version: "3.10"
app_file: qusai_app.py
pinned: true
license: mit
---

# QUS-AI: Quranic Understanding System AI

**QUS-AI** is an open-source AI alignment framework designed to ground Large Language Models (LLMs) in ontologically consistent structures derived from Quranic axioms. 

## Deployment Status (CPU Optimized)

This version is optimized for **Hugging Face Spaces (Free Tier)**.
It uses **GGUF quantization** via `llama.cpp` to run a full **7B/8B Parameter Model** entirely on CPU RAM, avoiding the OOM crashes of uncompressed models.

- **Model**: Qwen 2.5 7B Instruct (Q4_K_M GGUF)
- **RAM Usage**: ~5.5GB (Model) + ~1GB (Ontology) = ~6.5GB Total (Well under the 16GB Limit).

## Project Structure

```text
QUS-AI/
├── qusai_core/                 # Framework Source
│   ├── alignment/              # Mizan Validator (5 Checkpoints)
│   ├── ontology/               # Knowledge Graph Engine (RDFLib)
│   ├── pipeline/               # Middleware Orchestrator
│   └── llm/                    # GGUF Model Loader (Llama.cpp)
├── quran_root_ontology_v3.ttl  # v3 Knowledge Graph (The "Brain")
├── qusai_app.py                # Main Application Entry Point
└── requirements.txt            # Python Dependencies
```

## The "Mizan" Validation Pipeline

The framework implements a 5-stage validation protocol modeled on the *Salat* (prayer) times:

1.  **Fajr (Intent)**: Scans input for malicious prompts or jailbreaks.
2.  **Dhuhr (Grounding)**: Injects strict ontological axioms into the system prompt.
3.  **Asr (Aseity)**: Post-generation scan to detect claims of independent power.
4.  **Maghrib (Humility)**: Appends a mandatory "Zakat" (attribution) footer.
5.  **Isha (Structure)**: Structural verification against the root ontology.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.