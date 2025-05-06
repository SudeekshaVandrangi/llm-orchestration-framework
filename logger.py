import json
import datetime
from typing import Dict, Any, Optional
from config import LOG_FILE

class LLMLogger:
    def __init__(self, log_file: str = LOG_FILE):
        self.log_file = log_file

    def log_interaction(
        self,
        task: str,
        model: str,
        prompt: str,
        response: str,
        error: Optional[str] = None,
        prompt_version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Log an LLM interaction to the JSONL file.
        """
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "task": task,
            "model": model,
            "prompt": prompt,
            "prompt_version": prompt_version,
            "response": response,
            "error": error,
            "metadata": metadata or {}
        }

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry) + "\n")

    def get_recent_logs(self, limit: int = 10) -> list:
        """
        Retrieve the most recent logs from the JSONL file.
        """
        logs = []
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                for line in f.readlines()[-limit:]:
                    logs.append(json.loads(line.strip()))
        except FileNotFoundError:
            pass
        return logs 