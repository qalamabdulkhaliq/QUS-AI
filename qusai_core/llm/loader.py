import os
import logging
from typing import Tuple, Optional
from abc import ABC, abstractmethod

# Set verbosity before imports
os.environ['TRANSFORMERS_VERBOSITY'] = 'error'

logger = logging.getLogger(__name__)

class ModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 100) -> str:
        pass

    @abstractmethod
    def load(self):
        pass

class HuggingFaceModel(ModelInterface):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.tokenizer = None
        self.model = None
        self.is_ready = False
        
    def load(self):
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
        except ImportError:
            logger.warning("Torch/Transformers not installed. Running in Ontology-Only mode.")
            return

        token = os.environ.get("HF_TOKEN")
        logger.info(f"Loading model {self.model_id}...")
        
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_id, 
                token=token, 
                trust_remote_code=True
            )
            # CPU-friendly loading by default as per project preference
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_id,
                token=token,
                torch_dtype="auto",
                device_map="cpu",
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )
            self.model.eval()
            self.is_ready = True
            logger.info(f"Model {self.model_id} loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")

    def generate(self, prompt: str, max_new_tokens: int = 200) -> str:
        if not self.is_ready:
            return "[Model not loaded - Ontology Only]"

        import torch
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    do_sample=True,
                    temperature=0.7,
                    top_p=0.9
                )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Clean up prompt echo if present
            if prompt in response:
                response = response.replace(prompt, "", 1).strip()
            # Or strict "Answer:" splitting if prompt format dictates
            if "Answer:" in response:
                response = response.split("Answer:")[-1].strip()
                
            return response
        except Exception as e:
            logger.error(f"Generation failed: {e}")
            return f"Error during generation: {e}"
