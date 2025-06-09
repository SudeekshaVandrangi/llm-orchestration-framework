import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from typing import List, Dict, Any

# Initialize Firebase only once
if not firebase_admin._apps:
    cred = credentials.Certificate(st.secrets["FIREBASE"])
    firebase_admin.initialize_app(cred)
db = firestore.client()

def load_logs_firestore() -> List[Dict[str, Any]]:
    logs = []
    docs = db.collection('logs').order_by('timestamp', direction=firestore.Query.DESCENDING).stream()
    for doc in docs:
        logs.append(doc.to_dict())
    return logs

def get_unique_values(logs: List[Dict[str, Any]], key: str) -> List[str]:
    return sorted(list({log.get(key, "") for log in logs if key in log}))

def save_feedback(feedback_entry: Dict[str, Any]):
    db.collection('feedback').add(feedback_entry)

def main():
    st.title("LLM Orchestration Logs Dashboard + Feedback Loop")
    logs = load_logs_firestore()

    if not logs:
        st.info("No logs found.")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    tasks = ["All"] + get_unique_values(logs, "task")
    models = ["All"] + get_unique_values(logs, "model")
    prompt_versions = ["All"] + get_unique_values(logs, "prompt_version")

    selected_task = st.sidebar.selectbox("Task", tasks)
    selected_model = st.sidebar.selectbox("Model", models)
    selected_version = st.sidebar.selectbox("Prompt Version", prompt_versions)

    # Apply filters
    filtered_logs = logs
    if selected_task != "All":
        filtered_logs = [log for log in filtered_logs if log.get("task") == selected_task]
    if selected_model != "All":
        filtered_logs = [log for log in filtered_logs if log.get("model") == selected_model]
    if selected_version != "All":
        filtered_logs = [log for log in filtered_logs if log.get("prompt_version") == selected_version]

    st.write(f"Showing {len(filtered_logs)} log(s)")

    for i, log in enumerate(filtered_logs):
        with st.expander(f"[{log.get('timestamp', '')}] {log.get('task', '')} | {log.get('model', '')} | v{log.get('prompt_version', '')}"):
            st.markdown(f"**Timestamp:** {log.get('timestamp', '')}")
            st.markdown(f"**Task:** {log.get('task', '')}")
            st.markdown(f"**Model:** {log.get('model', '')}")
            st.markdown(f"**Prompt Version:** {log.get('prompt_version', '')}")
            st.markdown(f"**Error:** {log.get('error', '') if log.get('error') else 'None'}")
            st.markdown("**Metadata:**")
            st.code(json.dumps(log.get('metadata', {}), indent=2), language=None)
            st.markdown("**Prompt:**")
            st.code(log.get('prompt', ''), language=None)
            st.markdown("**Response:**")
            st.code(log.get('response', ''), language=None)

            # Feedback loop UI
            feedback_key = f"feedback_{i}"
            if st.button("Mark as Needs Improvement", key=feedback_key):
                st.session_state[f"show_feedback_form_{i}"] = True
            if st.session_state.get(f"show_feedback_form_{i}", False):
                with st.form(f"feedback_form_{i}"):
                    reason = st.selectbox(
                        "Reason for feedback:",
                        ["Vague response", "Poor follow-up", "Incorrect information", "Other"]
                    )
                    comment = st.text_area("Optional comment:")
                    submitted = st.form_submit_button("Submit Feedback")
                    if submitted:
                        feedback_entry = {
                            "log": log,
                            "reason": reason,
                            "comment": comment
                        }
                        save_feedback(feedback_entry)
                        st.success("Feedback submitted!")
                        st.session_state[f"show_feedback_form_{i}"] = False

if __name__ == "__main__":
    main() 