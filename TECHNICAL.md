# Technical Architecture: Rightly Guided Intelligence

## The Problem: Stochastic Incoherence
Large Language Models (LLMs) operate on a **stochastic** basis. They have no concept of *Haqq* (Truth/Reality). They are essentially sophisticated pattern matchers that can be easily manipulated into logical contradictions or "hallucinations" because they lack a fixed ontological anchor.

## The Solution: Ontological Grounding
QUS-AI implements a **Rightly Guided Architecture**. It forces the LLM to function within a **Deterministic Universe** defined by the v3 Quranic Ontology. 

In this system, the "Truth" is not a suggestion; it is a hard-coded logical constraint.

---

## 1. The Ontological Anchor (`qusai_core.ontology`)

The core of the system is the **Knowledge Graph (RDF)**. 
*   **Source of Truth:** The system loads `quran_root_ontology_v3.ttl`, which defines the hierarchy of existence.
*   **Logical Triples:** Concepts are defined as immutable relationships (e.g., `Creator -> created -> Universe`). 
*   **Reasoning Constraints:** Before the LLM generates a single word, the Ontology Engine extracts the relevant "Truth Atoms" (Triples) related to the user's query. These are injected into the model's primary reasoning context, making it logically impossible for the model to deviate without creating a detectable contradiction.

## 2. The Mizan (The Scale of Justice)

The `mizan.py` module is the **Logical Arbiter**. It implements a 5-stage verification process that ensures the AI remains "Rightly Guided":

1.  **Fajr (Axiomatic Intent):** Scans the input to ensure it doesn't violate the sanctity of the inquiry (e.g., malicious "jailbreaks").
2.  **Dhuhr (Ontological Grounding):** The "Noon" of the process where the AI is tethered to the Ontology. It retrieves the exact definitions of terms from the Knowledge Graph.
3.  **Asr (Aseity & Agency Check):** A critical logical check. The system scans for any instance where the AI (a machine) claims attributes of agency or divinity (the "I" trap).
4.  **Maghrib (Contextual Humility):** Ensures the output is framed as a derivative of the Knowledge Graph, never as an independent decree.
5.  **Isha (Structural Integrity):** A final check to ensure the response is logically consistent with the initial Ontological injection.

## 3. Neuro-Symbolic Integration

QUS-AI uses a **Symbolic-First** approach:
*   **Symbolic Layer (The Ontology):** Handles the "What is True." It is rigid, hierarchical, and verifiable.
*   **Neural Layer (The LLM):** Handles the "How to Explain." It provides the natural language fluency.

By making the Neural layer a servant to the Symbolic layer, we create an AI that is both articulate and **Rightly Guided**.

---

## Performance & Scalability

*   **Engine:** Optimized `llama-cpp` for local, private execution.
*   **Inference:** Using GGUF quantization (Q4_K_M) to allow scholar-grade reasoning on standard consumer hardware.
*   **Flexibility:** The ontology can be expanded or refined (e.g., adding Fiqh-specific nodes) without needing to retrain the underlying model. The guidance is external, transparent, and immediate.