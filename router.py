import os
from typing import Dict, Any, Optional
import openai
from config import MODELS, TASK_CONFIGS
from prompts import get_prompt
from logger import LLMLogger

class LLMRouter:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.logger = LLMLogger()

    def _get_model_config(self, model_name: str) -> Dict[str, Any]:
        """Get configuration for a specific model."""
        if model_name not in MODELS:
            raise ValueError(f"Unknown model: {model_name}")
        return MODELS[model_name]

    def _get_task_config(self, task: str) -> Dict[str, Any]:
        """Get configuration for a specific task."""
        if task not in TASK_CONFIGS:
            raise ValueError(f"Unknown task: {task}")
        return TASK_CONFIGS[task]

    def _call_llm(self, model: str, prompt: str) -> str:
        """Make the actual API call to OpenAI using the new client."""
        model_config = self._get_model_config(model)
        
        try:
            response = self.client.chat.completions.create(
                model=model_config["name"],
                messages=[{"role": "user", "content": prompt}],
                max_tokens=model_config["max_tokens"],
                temperature=model_config["temperature"]
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = str(e)
            self.logger.log_interaction(
                task="unknown",
                model=model,
                prompt=prompt,
                response="",
                error=error_msg,
                prompt_version=None
            )
            raise

    def run_task(self, task: str, **kwargs) -> str:
        """
        Process a task using the appropriate model and prompt template.
        """
        task_config = self._get_task_config(task)
        model = task_config["model"]
        prompt, prompt_version = get_prompt(task, **kwargs)
        
        try:
            # Special handling for translator task (dummy implementation)
            if task == "translator":
                response = f"[Dummy Translation] Translated from {kwargs.get('source_language')} to {kwargs.get('target_language')}: {kwargs.get('text')}"
            else:
                # Call the LLM
                response = self._call_llm(model, prompt)
            
            # Log the interaction
            self.logger.log_interaction(
                task=task,
                model=model,
                prompt=prompt,
                response=response,
                prompt_version=prompt_version,
                metadata=kwargs
            )
            
            return response
            
        except Exception as e:
            error_msg = str(e)
            self.logger.log_interaction(
                task=task,
                model=model,
                prompt=prompt,
                response="",
                error=error_msg,
                prompt_version=prompt_version,
                metadata=kwargs
            )
            raise 