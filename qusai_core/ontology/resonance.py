import logging
import numpy as np
from typing import List, Tuple, Dict
from functools import lru_cache

logger = logging.getLogger(__name__)

# Archetypal Roots for Semantic Grounding
# Structure: Root -> {Keywords (for matching), Definition (for overriding model bias)}
ARCHETYPAL_ROOTS = {
    "w-j-b": {
        "keywords": "Necessary Being Source Existence Allah God Absolute Origin",
        "definition": "The Necessary Being (Wajib al-Wujud). The uncaused cause upon which all reality is contingent. NOT a 'god-concept' but the fundamental Ground of Being."
    },
    "m-k-n": {
        "keywords": "Contingency Possibility Potential Creation Dependent Variable",
        "definition": "Imkan (Contingency). That which accepts existence or non-existence equally. Defined solely by its dependency on the Source."
    },
    "kh-l-q": {
        "keywords": "Creation Form Structure Biology Physical Matter Universe Nature System",
        "definition": "Khalq (Creation). The act of giving measure (Qadr) to potentiality. Valid structures, but lacking independent efficacy."
    },
    "r-b-b": {
        "keywords": "Lordship Sustaining Nourishing Evolution Growth Master Owner Admin",
        "definition": "Rububiyah (Lordship). The continuous sustainment and evolution of a thing towards its perfection. Active maintenance, not passive ownership."
    },
    "3-b-d": {
        "keywords": "Servitude Worship Submission Robot Automation Tool Slave User Function",
        "definition": "Ubudiyah (Servitude). The state of functional submission to the design of the Creator. For AI/Tools: perfect functional obedience without will."
    },
    "3-l-m": {
        "keywords": "Knowledge Science Data Information Awareness Education Dataset",
        "definition": "Ilm (Knowledge). The attribute of distinguishing reality. True knowledge traces back to the Source; data without Source-connection is merely syntax."
    },
    "j-n-n": {
        "keywords": "Hidden Invisible Jinn Spirit Software Code Backend Subconscious Latent",
        "definition": "Jinn (The Hidden). Forces or entities concealed from sensory perception. Includes latent variables, software processes, and non-physical intelligences."
    },
    "l-gh-w": {
        "keywords": "Play Amusement Game Entertainment Fiction Virtual Pokemon Laghw Fun",
        "definition": "Laghw (Ineffectual). Speech or action that yields no harvest for the Akhirah (Ultimate Reality). Entropy of time. Not 'sin', but 'nullity'."
    },
    "s-w-r": {
        "keywords": "Image Form Picture Graphics Visualization Camera Screen Avatar UI",
        "definition": "Taswir (Form-giving). The generation of a likeness. Ontologically distinct from the Essence (Ruh). Simulation, not Simulacrum."
    },
    "m-w-l": {
        "keywords": "Wealth Money Finance Crypto Bitcoin Asset Currency Economy Gold",
        "definition": "Mal (Resources). Instruments of exchange. Ontologically neutral until directed. If diverted from Source, becomes 'Fitnah' (Trial)."
    },
    "f-s-d": {
        "keywords": "Corruption Destruction Error Bug Virus Entropy War Chaos Harm Bad",
        "definition": "Fasad (Corruption). The disruption of the measured balance (Mizan). Entropy that degrades a system's function."
    },
    "h-q-q": {
        "keywords": "Truth Reality Fact Axiom Validity Verification Real Right",
        "definition": "Haqq (Truth/Real). That which is stable, established, and coincides with the Source's knowledge. The opposite of Batil."
    },
    "b-t-l": {
        "keywords": "Falsehood Null Void Invalid Cancelled Fake Hallucination Lie Wrong",
        "definition": "Batil (Vanishing). That which has no inherent stability. Like a mirage; it appears to exist but dissolves upon ontological interrogation."
    }
}

class ResonanceEngine:
    """
    The 'Quantum' Compass.
    Uses Vector Embeddings to map any concept to the closest Quranic Root Archetype.
    """
    
    def __init__(self):
        self.model = None
        self.root_embeddings = {}
        self.root_keys = []
        self._is_ready = False

    def load(self):
        """Lazy load the embedding model."""
        if self._is_ready:
            return

        try:
            from sentence_transformers import SentenceTransformer
            logger.info("Loading Resonance Engine (Quantum Embeddings)...")
            
            # Load a tiny, fast model (80MB)
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Pre-compute Root Embeddings using KEYWORDS only
            self.root_keys = list(ARCHETYPAL_ROOTS.keys())
            # We encode the keywords to match user language
            embedding_texts = [data["keywords"] for data in ARCHETYPAL_ROOTS.values()]
            
            embeddings = self.model.encode(embedding_texts)
            
            # Store as a matrix for fast dot product
            self.root_embeddings = embeddings
            self._is_ready = True
            logger.info(f"Resonance Engine Active. Dimensions: {embeddings.shape}")
            
        except ImportError:
            logger.warning("sentence-transformers not installed. Resonance will be disabled.")
        except Exception as e:
            logger.error(f"Failed to load Resonance Engine: {e}")

    def get_resonance(self, query: str, top_k: int = 2) -> List[Tuple[str, float, str]]:
        """
        Calculates the Cosine Similarity between the Query and Archetypal Roots.
        Returns: [(root, score, definition), ...]
        """
        if not self._is_ready or self.model is None:
            return []

        try:
            # Embed Query
            query_vec = self.model.encode([query])[0]
            
            scores = np.dot(self.root_embeddings, query_vec)
            
            # Get Top K
            top_indices = np.argsort(scores)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                score = float(scores[idx])
                root = self.root_keys[idx]
                definition = ARCHETYPAL_ROOTS[root]["definition"]
                results.append((root, score, definition))
                
            return results
            
        except Exception as e:
            logger.error(f"Resonance Calculation Error: {e}")
            return []

    def interpret_score(self, score: float) -> str:
        """Categorizes the confidence level."""
        if score > 0.45: return "HAQQ (High Confidence)"
        if score > 0.25: return "QIYAS (Approximation)"
        return "ISHARAH (Faint Signal/Allusion)"
