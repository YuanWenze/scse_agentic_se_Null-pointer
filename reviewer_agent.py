import json
from pathlib import Path
from ollama import chat

system_prompt = """
You are a reviewer agent for a mobile robot.
Read the simulation report in JSON format.
Output ONLY a JSON object. Do not write anything else.

The JSON must have exactly these keys:
"issue": a string
"likely_cause": a string
"recommendation": a string
"needs_revision": true or false
"""


def validate_review(data):
    if not isinstance(data, dict):
        return False

    keys = ["issue", "likely_cause", "recommendation", "needs_revision"]
    for key in keys:
        if key not in data:
            return False

    if not isinstance(data["needs_revision"], bool):
        return False
    if not isinstance(data["issue"], str):
        return False
    if not isinstance(data["likely_cause"], str):
        return False
    if not isinstance(data["recommendation"], str):
        return False

    return True


def run_reviewer(simulation_report):
    report_text = json.dumps(simulation_report)

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": report_text}
        ]
    )

    json_text = response.message.content
    review = json.loads(json_text)

    if validate_review(review):
        return review
    else:
        return None


if __name__ == "__main__":
    report_path = Path("artifacts/simulation_report.json")
    report_text = report_path.read_text(encoding="utf-8")
    report = json.loads(report_text)

    review = run_reviewer(report)

    if review is None:
        print("Review validation failed")
    else:
        output_path = Path("artifacts/review_report.json")
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(review, file, indent=2)

        print("Review saved")
        print(json.dumps(review, indent=2))