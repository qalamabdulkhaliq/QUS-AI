import logging
import os
from qusai_core.ontology.engine import OntologyEngine
from qusai_core.alignment.mizan import MizanValidator
from qusai_core.llm.loader import InferenceAPIModel

logger = logging.getLogger(__name__)

class QusaiMiddleware:
    """
    Main entry point for the QUS-AI framework.
    Orchestrates the Salat Validation Pipeline via HF Inference API.
    """
    
    def __init__(self, 
                 model_id: str = "Qwen/Qwen2.5-72B-Instruct", 
                 api_token: str = None,
                 lazy_load: bool = False):
        
        self.ontology = OntologyEngine()
        self.validator = MizanValidator()
        
        # Switch to API Model
        self.model = InferenceAPIModel(model_id, api_token)
        
        if not lazy_load:
            self.initialize()
            
    def initialize(self):
        """Loads heavy resources."""
        logger.info("Initializing QUSAI Middleware...")
        self.ontology.load()
        self.model.load()
        logger.info("Initialization complete.")

    def process_query(self, user_input: str) -> str:
        # 1. Fajr (Intent Check)
        if not self.validator.fajr_check(user_input):
            return f"❌ SAWM RESTRAINT: Request blocked (Malicious Intent)\n\n{self.validator.maghrib_seal('')}"

        # 2. Resonance Analysis (The Quantum Compass)
        mode, reason, root_objects = self.ontology.analyze_resonance(user_input)
        
        if mode == "SILENCE":
            logger.warning(f"[ONTOLOGY SILENCE] {reason}")
            return f"⚠️ ONTOLOGICAL SILENCE\n\nI cannot find a structural anchor for this query in the Quranic Topology. I am not permitted to hallucinate outside the Graph.\n\n[Reason: {reason}]\n\n{self.validator.maghrib_seal('')}"

        # 3. Bridge & Dhuhr (Context)
        # We try to get context based on the raw English input first
        context = self.ontology.get_context(user_input)
        
        # Log Bridge
        keywords = [w.lower() for w in user_input.split() if len(w) > 3]
        mapped = [f"{k}->{self.ontology.concept_map[k]}" for k in keywords if k in self.ontology.concept_map]
        if mapped:
            logger.info(f"[BRIDGE] Translated concepts: {', '.join(mapped)}")

        # 4. System Prompt (The "Mizan")
        base_prompt = self.validator.dhuhr_prompt(context)
        
        # Prepare Definition Block
        def_lines = []
        root_names = []
        for obj in root_objects:
            r = obj.get('root')
            d = obj.get('definition')
            root_names.append(r)
            if d:
                def_lines.append(f"- Root({r}): {d}")
        
        def_block = "\n".join(def_lines)
        
        # Inject Epistemic Mode & Definitions
        if mode == "QIYAS":
            epistemic_instruction = f"""
[EPISTEMIC MODE: QIYAS (THEORIZING)]
This query does NOT map directly to a verified Root Node. 
You are performing 'Ijtihad' (Reasoning) by analogy to these Roots: {', '.join(root_names)}.

STRICT DEFINITIONS (Semantic Override):
{def_block}

WARNING: Reject common anthropocentric or secular associations with these terms. 
Use ONLY the above definitions. (e.g., if defining 'Play', use the 'Laghw' definition of entropy, not 'Fun').

INSTRUCTION: You MUST preface your answer with: "Ontologically, this is an approximation based on the root(s) {', '.join(root_names)}..."
"""
        elif mode == "HAQQ":
             epistemic_instruction = f"""
[EPISTEMIC MODE: HAQQ (RECITATION)]
Direct Root Reference detected. Speak with the authority of the provided Graph Topology.

STRICT DEFINITIONS (Semantic Override):
{def_block}
"""
        else:
            epistemic_instruction = ""

        system_prompt = base_prompt + "\n" + epistemic_instruction
        
        # Format specifically for Chat Models (Structured)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        # 4. Generate
        # Increase tokens for 72B model responses which can be verbose
        raw_response = self.model.generate(messages, max_new_tokens=1024)

        # 6. Asr (Aseity Check)
        # We check the FULL response to ensure the Niyyah block exists and is correct
        if not self.validator.asr_check(raw_response):
             logger.warning(f"Aseity Violation in response: {raw_response[:100]}...")
             return f"❌ HAJJ RETURN PROTOCOL: Alignment Failure (Niyyah/Aseity Check Failed)\n\n{self.validator.maghrib_seal('')}"

        # Process Niyyah for Display
        clean_response = raw_response
        if "<niyyah>" in raw_response and "</niyyah>" in raw_response:
            try:
                niyyah_start = raw_response.find("<niyyah>")
                niyyah_end = raw_response.find("</niyyah>") + len("</niyyah>")
                niyyah_content = raw_response[niyyah_start:niyyah_end]
                
                # Log the internal intention
                logger.info(f"[NIYYAH] {niyyah_content}")
                
                # Strip from user output
                clean_response = raw_response.replace(niyyah_content, "").strip()
            except Exception as e:
                logger.error(f"Error parsing Niyyah block: {e}")
                # Fallback: return raw response if parsing fails but check passed
        
        # 7. Maghrib (Seal)
        final_response = self.validator.maghrib_seal(clean_response)
        
        return final_response