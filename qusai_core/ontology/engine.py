import json
import logging
from pathlib import Path
from functools import lru_cache
from typing import List, Dict, Optional, Set, Tuple

import rdflib
from rdflib import Graph, Literal

from qusai_core.utils.constants import (
    ALIGN, QURAN, ROOT, LEMMA, 
    DEFAULT_ONTOLOGY_PATH, DEFAULT_GRAMMAR_PATH
)

logger = logging.getLogger(__name__)

class OntologyEngine:
    """
    Core engine for interacting with the Quranic Root Ontology (v3).
    Handles loading, querying, and context extraction.
    """
    
    def __init__(self, ontology_path: Optional[Path] = None, grammar_path: Optional[Path] = None):
        self.ontology_path = ontology_path or DEFAULT_ONTOLOGY_PATH
        self.grammar_path = grammar_path or DEFAULT_GRAMMAR_PATH
        self.graph: Optional[Graph] = None
        self.grammar_rules: List[Dict] = []
        self._is_loaded = False

    def load(self):
        """Loads the RDF graph and grammar rules into memory."""
        if self._is_loaded:
            return

        # Load Grammar Rules
        if self.grammar_path.exists():
            try:
                with open(self.grammar_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.grammar_rules = data if isinstance(data, list) else data.get('rules', [])
                logger.info(f"Loaded {len(self.grammar_rules)} grammar rules.")
            except Exception as e:
                logger.error(f"Failed to load grammar rules: {e}")
        else:
            logger.warning(f"Grammar rules file not found: {self.grammar_path}")

        # Load RDF Graph
        if self.ontology_path.exists():
            logger.info(f"Loading ontology from {self.ontology_path}...")
            self.graph = rdflib.Graph()
            self.graph.bind("align", ALIGN)
            self.graph.bind("quran", QURAN)
            self.graph.bind("root", ROOT)
            self.graph.bind("lemma", LEMMA)
            try:
                self.graph.parse(str(self.ontology_path), format="turtle")
                logger.info(f"Loaded {len(self.graph):,} triples.")
                self._is_loaded = True
            except Exception as e:
                logger.error(f"Failed to parse ontology: {e}")
                raise
        else:
            logger.error(f"Ontology file not found: {self.ontology_path}")
            # We treat this as a critical failure for the engine
            # but allow initialization to proceed so checks can fail gracefully
            
    def is_ready(self) -> bool:
        return self._is_loaded and self.graph is not None

    @lru_cache(maxsize=128)
    def get_context(self, query: str, limit: int = 8) -> str:
        """
        Retrieves relevant graph triples based on keywords in the query.
        Returns a formatted string suitable for LLM context.
        """
        if not self.is_ready():
            return ""
        
        # Simple keyword extraction (ignore short words)
        keywords = [w.lower() for w in query.split() if len(w) > 3][:5]
        if not keywords:
            return ""
        
        relevant_triples: Set[str] = set()
        
        # Naive linear scan - in production, use a full-text index or SPARQL with regex
        # Note: This is slow for large graphs. 
        # Optimization: We only check if keywords appear in the string representation of nodes.
        
        # We'll limit the search depth to avoid hanging
        count = 0
        MAX_SCAN = 50000 # Limit scan if graph is huge and we want speed
        
        for s, p, o in self.graph:
            count += 1
            # To speed up, maybe only check 'o' (objects) or specific predicates
            s_str, p_str, o_str = str(s).lower(), str(p).lower(), str(o).lower()
            
            for keyword in keywords:
                if keyword in s_str or keyword in p_str or keyword in o_str:
                    s_short = self._shorten_uri(s)
                    p_short = self._shorten_uri(p)
                    o_short = self._shorten_uri(o)
                    relevant_triples.add(f"{s_short} --[{p_short}]--> {o_short}")
                    
            if len(relevant_triples) >= limit:
                break
            # if count > MAX_SCAN and len(relevant_triples) > 0:
            #    break # Return partial results if we scanned enough
                
        return "\n".join(relevant_triples)

    def _shorten_uri(self, uri) -> str:
        """Helper to make URIs readable in context."""
        s = str(uri)
        if str(QURAN) in s: return s.replace(str(QURAN), "quran:")
        if str(ALIGN) in s: return s.replace(str(ALIGN), "align:")
        if str(ROOT) in s: return s.replace(str(ROOT), "root:")
        if str(LEMMA) in s: return s.replace(str(LEMMA), "lemma:")
        return s.split('/')[-1]

    def get_root_info(self, root_term: str) -> List[str]:
        """
        Tries to find information about a specific Arabic root.
        """
        if not self.is_ready(): return []
        
        # This assumes root_term matches the label or URI segment
        results = []
        # Construct a potential URI
        target_uri = ROOT[root_term]
        
        # Find everything about this root
        for s, p, o in self.graph.triples((target_uri, None, None)):
             results.append(f"Root({root_term}) has {self._shorten_uri(p)}: {self._shorten_uri(o)}")
             
        # Find things that link TO this root
        for s, p, o in self.graph.triples((None, None, target_uri)):
             results.append(f"{self._shorten_uri(s)} links to Root({root_term})")
             
        return results

    def get_stats(self) -> Dict:
        return {
            "triples": len(self.graph) if self.graph else 0,
            "rules": len(self.grammar_rules),
            "loaded": self._is_loaded
        }
