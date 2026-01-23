import os
import logging
from abc import ABC, abstractmethod
from huggingface_hub import InferenceClient

logger = logging.getLogger(__name__)

class ModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        pass
    
    @abstractmethod
    def load(self):
        pass

class InferenceAPIModel(ModelInterface):
    """
    Uses the Hugging Face Serverless Inference API.
    Accesses 70B+ models using the Pro Subscription benefits.
    """
    def __init__(self, model_id: str, api_token: str = None):
        self.model_id = model_id
        # Use provided token or fallback to environment variable
        self.token = api_token or os.environ.get("HF_TOKEN")
        self.client = None

    def load(self):
        if not self.token:
            logger.warning("⚠️ No HF_TOKEN found! Rate limits will be low (Free Tier). Add HF_TOKEN to Space secrets for Pro speeds.")
        
        logger.info(f"Connecting to Serverless Inference API: {self.model_id}")
        self.client = InferenceClient(model=self.model_id, token=self.token)
        logger.info("✓ API Client Ready")

    def generate(self, prompt: str | list, max_new_tokens: int = 512) -> str:
        if not self.client:
            self.load()
            
        try:
            # If prompt is a string, wrap it in a user message (fallback)
            messages = prompt
            if isinstance(prompt, str):
                messages = [{"role": "user", "content": prompt}]

            # Use chat_completion which is native for Instruct models
            response = self.client.chat_completion(
                messages=messages,
                max_tokens=max_new_tokens,
                temperature=0.7,
                top_p=0.9,
                stream=False
            )
            
            # Extract content from the response object
            return response.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"API Generation Error: {e}")
            return f"Error: {e} (Check HF_TOKEN or Model Status)"

# Legacy GGUF class removed to keep dependencies light. 
# If local fallback is needed, re-add llama-cpp-python logic here.