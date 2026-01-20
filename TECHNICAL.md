# QUS-AI Framework Architecture

This document outlines the modular architecture for QUS-AI v2, leveraging the v3 Ontology.

## Core Package Structure (`qusai_core/`)

The framework is organized as a modular Python package:

- **`ontology/`**: Manages the Quranic Knowledge Graph (v3).
  - `engine.py`: Loads the `.ttl` file and provides `get_context()` and `get_root_info()` methods.
- **`alignment/`**: Implements the "Mizan" (Balance) logic.
  - `mizan.py`: Contains the 5 Checkpoints (Salat Pattern): Fajr, Dhuhr, Asr, Maghrib, Isha.
- **`llm/`**: Abstraction for Model Loading.
  - `loader.py`: Supports HuggingFace models (optimized for CPU/Apple Silicon). Extensible for API integration.
- **`pipeline/`**: Core execution logic.
  - `middleware.py`: Orchestrates the flow: User Input -> Validator -> Ontology -> Model -> Validator -> Output.

## Usage

### Running the Application
```bash
python qusai_app.py
```

### Library Integration
```python
from qusai_core.pipeline.middleware import QusaiMiddleware

# Initialize
qusai = QusaiMiddleware(model_id="Qwen/Qwen2.5-3B-Instruct")

# Query
response = qusai.process_query("What is the nature of Iblis?")
print(response)
```

## v3 Features
- **Root Lookup**: The engine binds specifically to the v3 Root namespace.
- **Type Safety**: Utilizes Python type hints for reliability.
- **Modularity**: Decoupled LLM and Ontology components allow for independent updates without affecting application logic.
