from typing import Dict, Tuple

PROMPT_TEMPLATES: Dict[str, Dict[str, str]] = {
    "moderator": {
        "template": """You are a content moderator. Review the following content for any inappropriate, harmful, or unsafe material.\n\nContent: {content}\n\nPlease analyze the content and provide:\n1. A safety assessment\n2. Any concerning elements\n3. Recommendations for improvement\n\nYour response:""",
        "version": "v1.0"
    },
    "theme_coder": {
        "template": """You are an expert at extracting key emotional or conceptual themes from user feedback.\n\nGiven the following feedback, identify and summarize the main themes (e.g., frustration with onboarding, joy around collaboration tools, confusion about pricing, etc.):\n\nFeedback: {requirements}\n\nPlease provide:\n1. A list of the main themes you identified\n2. A brief explanation for each theme\n3. Any suggestions for addressing negative themes\n\nYour response:""",
        "version": "v1.0"
    },
    "translator": {
        "template": """You are a translator. Translate the following text from {source_language} to {target_language}:\n\nText: {text}\n\nPlease provide:\n1. The translated text\n2. Any cultural context notes if relevant\n\nYour response:""",
        "version": "v1.0"
    }
}

def get_prompt(task: str, **kwargs) -> Tuple[str, str]:
    """
    Returns the rendered prompt and its version for the given task.
    """
    if task not in PROMPT_TEMPLATES:
        raise ValueError(f"No prompt template found for task: {task}")
    template = PROMPT_TEMPLATES[task]["template"]
    version = PROMPT_TEMPLATES[task]["version"]
    return template.format(**kwargs), version 