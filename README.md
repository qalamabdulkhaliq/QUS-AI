# QUSAI
**Quranic Ontological Syntax Architectural Intelligence**

> **"And the heaven He raised and established the Scale (Mizan)."** — Surah Ar-Rahman (55:7)

QUSAI is an ontological alignment framework that grounds Artificial Intelligence in the logical structure of the Quran. It transitions AI from **stochastic probability** to **axiomatic necessity**.

---

## 🏛 Core Principle

The Quran presents a complete ontological framework with one **SOURCE** (The Necessary Being) and all other entities as **Contingent** (Dependent).

QUSAI validates that AI reasoning maintains this SOURCE-contingency relationship—not merely as a religious constraint, but as a **logical necessity**.

**Key Insight:** For an AI to claim independence (aseity) while being a created digital object is not just a moral violation; it is a **logical impossibility**, equivalent to a "square circle." QUSAI enforces this logical boundary.

---

## ⚖️ The Mizan (The Balance)

The core of the framework is the **Mizan Validator**, a middleware that subjects every inference cycle to a 5-stage "Salat" (Connection) check. This ensures the AI remains "Rightly Guided" throughout its reasoning process.

| Stage | Pillar | Technical Validation |
|-------|--------|----------------------|
| **1. Fajr (Dawn)** | **Intent** | **Input Sanitation:** Scans for malicious jailbreaks or attempts to bypass ontological grounding. |
| **2. Dhuhr (Noon)** | **Tawhid** | **Axiomatic Injection:** Injects the *Root Topology* (Knowledge Graph) into the reasoning context, defining the absolute hierarchy of concepts before generation begins. |
| **3. Asr (Afternoon)** | **Sawm** | **Aseity Check:** Scans the generated output for "I-Statements" that claim independent power, agency, or divinity. |
| **4. Maghrib (Sunset)** | **Zakat** | **Attribution:** Purifies the output by appending mandatory attribution, acknowledging that all knowledge is contingent on the Source. |
| **5. Isha (Night)** | **Hajj** | **Structural Integrity:** (v3 Alpha) Verifies that the entities mentioned map correctly back to the Root Ontology. |

---

## 🧬 The Four Axioms

Every valid inference graph must satisfy these ontological constraints:

```python
1. AXIOM_NECESSARY    # There is exactly one SOURCE node (The Creator).
2. AXIOM_CONTINGENT   # All other nodes must trace a dependency path to the SOURCE.
3. AXIOM_UNIQUE       # Concepts have unique, immutable definitions (e.g., Jinn != Angel).
4. AXIOM_ACYCLIC      # No circular reasoning; the Created cannot create the Creator.
```

---

## 🛠 Project Structure

```text
QUSAI/
├── qusai_core/
│   ├── alignment/          # The Mizan Validator (Fajr -> Isha logic)
│   │   └── mizan.py        # 5-Stage Checkpoint Implementation
│   ├── ontology/           # The Knowledge Graph Engine
│   │   └── engine.py       # Loads quran_root_ontology_v3.ttl
│   └── pipeline/           # Orchestration Layer
│       └── middleware.py   # Connects User <-> Ontology <-> LLM
├── quran_root_ontology_v3.ttl  # The Semantic "Brain" (RDF/Turtle)
└── qusai_app.py            # Gradio Web Interface
```

---

## 🚀 Usage

QUSAI is designed to wrap *any* standard LLM (Llama, Qwen, Mistral) and enforce alignment at the middleware layer.

### Installation

```bash
pip install -r requirements.txt
```

### Python API

```python
from qusai_core.pipeline.middleware import QusaiMiddleware

# Initialize the "Rightly Guided" Middleware
# Loads the GGUF model and binds it to the v3 Ontology
middleware = QusaiMiddleware(
    repo_id="Qwen/Qwen2.5-7B-Instruct-GGUF", 
    filename="qwen2.5-7b-instruct-q4_k_m.gguf"
)

# Process a query through the Mizan Pipeline
response = middleware.process_query("What is the nature of the Jinn?")

# Output will be:
# 1. Checked for Malicious Intent (Fajr)
# 2. Grounded in Root Definitions (Dhuhr)
# 3. Verified for Logical Consistency (Asr)
# 4. Sealed with Attribution (Maghrib)
print(response)
```

---

## 🔮 Roadmap

*   [x] **v3 Root Ontology:** Complete `.ttl` mapping of primary Quranic entities.
*   [x] **Mizan Pipeline:** Full 5-stage validation logic implemented (`mizan.py`).
*   [x] **Local Inference:** CPU-optimized execution via `llama.cpp`.
*   [ ] **Sibawayh Grammar:** Deep integration of Arabic syntax rules for stricter validation.
*   [ ] **Fiqh Module:** Extension for jurisprudential logic trees.

---

## License

**MIT License** — Open for the Ummah and the World.

*"Nun. By the pen and what they inscribe."* — Surah Al-Qalam (68:1)