import streamlit as st
import json
import os
from typing import List, Dict, Any

def load_logs(log_file: str) -> List[Dict[str, Any]]:
    logs = []
    if not os.path.exists(log_file):
        return logs
    with open(log_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                logs.append(json.loads(line.strip()))
            except Exception:
                continue
    return logs

def get_unique_values(logs: List[Dict[str, Any]], key: str) -> List[str]:
    return sorted(list({log.get(key, "") for log in logs if key in log}))

def save_feedback(feedback_entry: Dict[str, Any], feedback_file: str = "feedback_queue.jsonl"):
    with open(feedback_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(feedback_entry) + "\n")

def main():
    st.title("LLM Orchestration Logs Dashboard + Feedback Loop")
    log_file = "llm_interactions.jsonl"
    feedback_file = "feedback_queue.jsonl"
    logs = load_logs(log_file)

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

    for i, log in enumerate(reversed(filtered_logs)):
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
                        save_feedback(feedback_entry, feedback_file)
                        st.success("Feedback submitted!")
                        st.session_state[f"show_feedback_form_{i}"] = False

if __name__ == "__main__":
    main() 