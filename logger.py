import json
import datetime
from typing import Dict, Any, Optional
# from config import LOG_FILE  # No longer needed
import firebase_admin
from firebase_admin import credentials, firestore
import os
import streamlit as st

class LLMLogger:
    def __init__(self):
        # Initialize Firestore only once
        if not firebase_admin._apps:
            cred = credentials.Certificate(st.secrets["FIREBASE"])
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

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
        Log an LLM interaction to Firestore.
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
        self.db.collection('logs').add(log_entry)

    def get_recent_logs(self, limit: int = 10) -> list:
        """
        Retrieve the most recent logs from Firestore.
        """
        logs = []
        docs = self.db.collection('logs').order_by('timestamp', direction=firestore.Query.DESCENDING).limit(limit).stream()
        for doc in docs:
            logs.append(doc.to_dict())
        return logs 