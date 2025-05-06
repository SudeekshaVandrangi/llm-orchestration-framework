import json

REQUIRED_FIELDS = ["task", "prompt", "response", "reason"]

feedback_file = "feedback_queue.jsonl"

def validate_feedback_entries():
    try:
        with open(feedback_file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f, 1):
                try:
                    entry = json.loads(line.strip())
                except Exception:
                    print(f"❌ Entry {idx} is not valid JSON.")
                    continue

                # The log is nested under 'log' in the feedback entry
                log = entry.get("log", {})
                reason = entry.get("reason")
                missing = []
                if not log.get("task"):
                    missing.append("task")
                if not log.get("prompt"):
                    missing.append("prompt")
                if not log.get("response"):
                    missing.append("response")
                if not reason:
                    missing.append("reason")
                if missing:
                    print(f"❌ Entry {idx} is missing fields: {missing}")
                else:
                    print(f"✅ Entry {idx} is valid.")
    except FileNotFoundError:
        print(f"File {feedback_file} not found.")

if __name__ == "__main__":
    validate_feedback_entries() 