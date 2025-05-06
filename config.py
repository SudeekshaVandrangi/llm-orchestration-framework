from typing import Dict, Any

# Model configurations
MODELS = {
    "gpt-4": {
        "name": "gpt-4",
        "max_tokens": 2000,
        "temperature": 0.7
    },
    "gpt-3.5-turbo": {
        "name": "gpt-3.5-turbo",
        "max_tokens": 1000,
        "temperature": 0.7
    }
}

# Task configurations mapping tasks to models
TASK_CONFIGS = {
    "moderator": {
        "model": "gpt-4",
        "description": "Content moderation and safety checks"
    },
    "theme_coder": {
        "model": "gpt-4",
        "description": "Code generation and theme development"
    },
    "translator": {
        "model": "gpt-3.5-turbo",
        "description": "Text translation (dummy implementation)"
    }
}

# Logging configuration
LOG_FILE = "llm_interactions.jsonl" 