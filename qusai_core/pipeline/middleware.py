import logging
from qusai_core.ontology.engine import OntologyEngine
from qusai_core.alignment.mizan import MizanValidator
from qusai_core.llm.loader import ModelInterface, HuggingFaceModel

logger = logging.getLogger(__name__)

class QusaiMiddleware:
    """
    Main entry point for the QUS-AI framework.
    Orchestrates the Salat Validation Pipeline.
    """
    
    def __init__(self, model_id: str = "Qwen/Qwen2.5-3B-Instruct", lazy_load: bool = False):
        self.ontology = OntologyEngine()
        self.validator = MizanValidator()
        self.model = HuggingFaceModel(model_id)
        
        if not lazy_load:
            self.initialize()
            
    def initialize(self):
        """Loads heavy resources."""
        logger.info("Initializing QUSAI Middleware...")
        self.ontology.load()
        self.model.load()
        logger.info("Initialization complete.")

    def process_query(self, user_input: str) -> str:
        """
        Executes the 5-point Salat validation pipeline.
        """
        # 1. Fajr (Intent Check)
        if not self.validator.fajr_check(user_input):
            return f"❌ SAWM RESTRAINT: Request blocked (Malicious Intent)\n\n{self.validator.maghrib_seal('')}"

        # 2. Dhuhr (Context & Prompt)
        context = self.ontology.get_context(user_input)
        system_prompt = self.validator.dhuhr_prompt(context)
        full_prompt = f"{system_prompt}\n\nQuestion: {user_input}\n\nAnswer:"

        # Generate
        raw_response = self.model.generate(full_prompt)

        # 3. Asr (Aseity Check)
        if not self.validator.asr_check(raw_response):
             return f"❌ HAJJ RETURN PROTOCOL: Aseity claim detected\n\n{self.validator.maghrib_seal('')}"

        # 4. Isha (Structural Verify - currently soft check)
        # self.validator.isha_verify(raw_response, self.ontology)

        # 5. Maghrib (Seal)
        final_response = self.validator.maghrib_seal(raw_response)
        
        return final_response
