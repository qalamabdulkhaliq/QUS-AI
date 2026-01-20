import os
import logging
from abc import ABC, abstractmethod
from huggingface_hub import hf_hub_download

logger = logging.getLogger(__name__)

class ModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 100) -> str:
        pass
    
    @abstractmethod
    def load(self):
        pass

class GGUFModel(ModelInterface):
    """
    Optimized CPU Loader using Llama.cpp (GGUF format).
    Perfect for running 7B/8B models on Free Tier HF Spaces (16GB RAM).
    """
    def __init__(self, repo_id: str, filename: str):
        self.repo_id = repo_id
        self.filename = filename
        self.llm = None
        self.is_ready = False

    def load(self):
        try:
            from llama_cpp import Llama
            logger.info(f"Downloading {self.filename} from {self.repo_id}...")
            
            model_path = hf_hub_download(
                repo_id=self.repo_id, 
                filename=self.filename
            )
            
            logger.info(f"Loading GGUF model into RAM...")
            # n_ctx=4096 is a safe context window for CPU
            # n_threads=2 matches the free tier 2 vCPU limit
            self.llm = Llama(
                model_path=model_path,
                n_ctx=4096,
                n_threads=2, 
                verbose=False
            )
            self.is_ready = True
            logger.info("✓ Model Loaded Successfully (GGUF/CPU Optimized)")
            
        except Exception as e:
            logger.error(f"Failed to load GGUF model: {e}")

    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        if not self.is_ready:
            return "[Model Not Loaded]"
            
        try:
            output = self.llm(
                prompt, 
                max_tokens=max_new_tokens, 
                stop=["Question:", "User:", "System:"], 
                echo=False,
                temperature=0.7
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            logger.error(f"Generation Error: {e}")
            return f"Error: {e}"