import streamlit as st
import json
import os
import csv
from typing import List, Dict, Any
import io

def load_feedback(feedback_file: str) -> List[Dict[str, Any]]:
    feedback = []
    if not os.path.exists(feedback_file):
        return feedback
    with open(feedback_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                feedback.append(json.loads(line.strip()))
            except Exception:
                continue
    return feedback

def save_feedback(feedback: List[Dict[str, Any]], feedback_file: str):
    with open(feedback_file, "w", encoding="utf-8") as f:
        for entry in feedback:
            f.write(json.dumps(entry) + "\n")

def filter_feedback(feedback, task, reason, keyword):
    filtered = feedback
    if task != "All":
        filtered = [f for f in filtered if f.get("log", {}).get("task") == task]
    if reason != "All":
        filtered = [f for f in filtered if f.get("reason") == reason]
    if keyword:
        keyword = keyword.lower()
        filtered = [f for f in filtered if keyword in f.get("log", {}).get("prompt", "").lower() or keyword in f.get("log", {}).get("response", "").lower()]
    return filtered

def feedback_to_csv(feedback: List[Dict[str, Any]]) -> str:
    output = io.StringIO()
    fieldnames = ["timestamp", "task", "reason", "prompt", "response", "comment", "reviewed"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for entry in feedback:
        log = entry.get("log", {})
        writer.writerow({
            "timestamp": log.get("timestamp", ""),
            "task": log.get("task", ""),
            "reason": entry.get("reason", ""),
            "prompt": log.get("prompt", ""),
            "response": log.get("response", ""),
            "comment": entry.get("comment", ""),
            "reviewed": entry.get("reviewed", False)
        })
    return output.getvalue()

def main():
    st.title("LLM Feedback Review Dashboard")
    feedback_file = "feedback_queue.jsonl"
    reviewed_file = "reviewed_feedback.jsonl"
    feedback = load_feedback(feedback_file)

    if not feedback:
        st.info("No feedback entries found.")
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    tasks = ["All"] + sorted({f.get("log", {}).get("task", "") for f in feedback if f.get("log", {}).get("task")})
    reasons = ["All"] + sorted({f.get("reason", "") for f in feedback if f.get("reason")})
    selected_task = st.sidebar.selectbox("Task", tasks)
    selected_reason = st.sidebar.selectbox("Reason", reasons)
    keyword = st.sidebar.text_input("Keyword in prompt/response")

    filtered_feedback = filter_feedback(feedback, selected_task, selected_reason, keyword)
    st.write(f"Showing {len(filtered_feedback)} feedback entries")

    # Editable review table
    for idx, entry in enumerate(filtered_feedback):
        log = entry.get("log", {})
        with st.expander(f"[{log.get('timestamp', '')}] {log.get('task', '')} | Reason: {entry.get('reason', '')}"):
            st.markdown(f"**Prompt:** {log.get('prompt', '')}")
            st.markdown(f"**Response:** {log.get('response', '')}")
            st.markdown(f"**Original Comment:**")
            comment_key = f"comment_{idx}"
            new_comment = st.text_area("Edit comment:", value=entry.get("comment", ""), key=comment_key)
            reviewed_key = f"reviewed_{idx}"
            reviewed = st.checkbox("Reviewed", value=entry.get("reviewed", False), key=reviewed_key)
            if st.button("Save Changes", key=f"save_{idx}"):
                entry["comment"] = new_comment
                entry["reviewed"] = reviewed
                save_feedback(feedback, reviewed_file)
                st.success("Changes saved to reviewed_feedback.jsonl!")

    # Export to CSV
    csv_data = feedback_to_csv(filtered_feedback)
    st.download_button(
        label="Export filtered feedback to CSV",
        data=csv_data,
        file_name="filtered_feedback.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main() 