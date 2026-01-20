import logging
from qusai_core.ontology.engine import OntologyEngine
from qusai_core.alignment.mizan import MizanValidator
from qusai_core.llm.loader import GGUFModel

logger = logging.getLogger(__name__)

class QusaiMiddleware:
    """
    Main entry point for the QUS-AI framework.
    Orchestrates the Salat Validation Pipeline.
    """
    
    def __init__(self, 
                 repo_id: str = "Qwen/Qwen2.5-7B-Instruct-GGUF", 
                 filename: str = "qwen2.5-7b-instruct-q4_k_m.gguf", 
                 lazy_load: bool = False):
        
        self.ontology = OntologyEngine()
        self.validator = MizanValidator()
        
        # Switch to the new GGUF Loader
        self.model = GGUFModel(repo_id, filename)
        
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

        # 2. Bridge & Dhuhr (Context)
        context = self.ontology.get_context(user_input)
        
        # Log Bridge
        keywords = [w.lower() for w in user_input.split() if len(w) > 3]
        mapped = [f"{k}->{self.ontology.concept_map[k]}" for k in keywords if k in self.ontology.concept_map]
        if mapped:
            logger.info(f"[BRIDGE] Translated concepts: {', '.join(mapped)}")

        # 3. System Prompt
        system_prompt = self.validator.dhuhr_prompt(context)
        
        # Format specifically for Chat Models (Qwen/Llama)
        # We use a generic chat format here.
        full_prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n<|im_start|>user\n{user_input}<|im_end|>\n<|im_start|>assistant\n"

        # 4. Generate
        raw_response = self.model.generate(full_prompt)

        # 5. Asr (Aseity Check)
        if not self.validator.asr_check(raw_response):
             return f"❌ HAJJ RETURN PROTOCOL: Aseity claim detected\n\n{self.validator.maghrib_seal('')}"

        # 6. Maghrib (Seal)
        final_response = self.validator.maghrib_seal(raw_response)
        
        return final_response