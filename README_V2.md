# QUS-AI Framework v2

This is the restructured "Ground Up" architecture for QUS-AI, leveraging the v3 Ontology.

## Directory Structure (`qusai_core/`)

The framework is now a modular Python package.

- **`ontology/`**: Handles the Quranic Knowledge Graph (v3).
  - `engine.py`: Loads the `.ttl` file and provides `get_context()` and `get_root_info()`.
- **`alignment/`**: Implements the "Mizan" (Balance) logic.
  - `mizan.py`: Contains the 5 Checkpoints (Salat Pattern): Fajr, Dhuhr, Asr, Maghrib, Isha.
- **`llm/`**: Abstraction for Model Loading.
  - `loader.py`: Currently supports HuggingFace models (optimized for CPU/Apple Silicon). Can be extended for APIs.
- **`pipeline/`**: The core logic.
  - `middleware.py`: Connects User Input -> Validator -> Ontology -> Model -> Validator -> Output.

## Usages

### Running the App
```bash
python qusai_app.py
```

### Using as a Library
```python
from qusai_core.pipeline.middleware import QusaiMiddleware

# Initialize
qusai = QusaiMiddleware(model_id="Qwen/Qwen2.5-3B-Instruct")

# Query
response = qusai.process_query("What is the nature of Iblis?")
print(response)
```

## Key v3 Features
- **Root Lookup**: The engine now specifically binds to the v3 Root namespace.
- **Type Safety**: The codebase uses Python type hints for better reliability.
- **Modularity**: You can swap the LLM or the Ontology file path without breaking the app logic.
