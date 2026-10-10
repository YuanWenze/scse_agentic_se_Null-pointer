import json
from pathlib import Path
from ollama import chat

system_prompt = """
You are a reviewer agent for a mobile robot benchmark.
Read the benchmark report and a deterministic review.
Output ONLY a JSON object. Do not write anything else.

The JSON must have exactly these keys:
"issue": a string
"likely_cause": a string
"recommendation": a string
"safety_passed": true or false
"goal_completion_passed": true or false
"efficiency_passed": true or false
"needs_revision": true or false
"""


def validate_review(data):
    if not isinstance(data, dict):
        raise ValueError("Review is not a dictionary")

    keys = ["issue", "likely_cause", "recommendation",
            "safety_passed", "goal_completion_passed",
            "efficiency_passed", "needs_revision"]
    for key in keys:
        if key not in data:
            raise ValueError("Missing key: " + key)

    if not isinstance(data["safety_passed"], bool):
        raise ValueError("safety_passed is not a boolean")
    if not isinstance(data["goal_completion_passed"], bool):
        raise ValueError("goal_completion_passed is not a boolean")
    if not isinstance(data["efficiency_passed"], bool):
        raise ValueError("efficiency_passed is not a boolean")
    if not isinstance(data["needs_revision"], bool):
        raise ValueError("needs_revision is not a boolean")

    if not isinstance(data["issue"], str):
        raise ValueError("issue is not a string")
    if not isinstance(data["likely_cause"], str):
        raise ValueError("likely_cause is not a string")
    if not isinstance(data["recommendation"], str):
        raise ValueError("recommendation is not a string")

    return True


def build_deterministic_review(benchmark_report):
    results = benchmark_report.get("results", [])

    safety_passed = True
    for report in results:
        if report.get("collision_or_done", False) and not report.get("reached_goal", False):
            safety_passed = False

    success_rate = benchmark_report.get("success_rate", 1.0)
    if success_rate >= 1.0:
        goal_completion_passed = True
    else:
        goal_completion_passed = False

    inefficient_success = benchmark_report.get("inefficient_success_worlds", 0)
    efficiency_rate = benchmark_report.get("efficiency_rate", 1.0)
    if inefficient_success == 0 and efficiency_rate >= 1.0:
        efficiency_passed = True
    else:
        efficiency_passed = False

    if not safety_passed:
        issue = "Unsafe benchmark behavior detected"
    elif not goal_completion_passed:
        issue = "Goal completion failure"
    elif not efficiency_passed:
        issue = "Successful but inefficient navigation"
    else:
        issue = "No issue"

    if safety_passed and goal_completion_passed and efficiency_passed:
        needs_revision = False
    else:
        needs_revision = True

    review = {
        "issue": issue,
        "likely_cause": "Navigation logic may not handle all states",
        "recommendation": "Consider revising the navigation logic",
        "safety_passed": safety_passed,
        "goal_completion_passed": goal_completion_passed,
        "efficiency_passed": efficiency_passed,
        "needs_revision": needs_revision
    }

    return review


def run_reviewer(benchmark_report):
    deterministic = build_deterministic_review(benchmark_report)

    payload = {
        "benchmark_report": benchmark_report,
        "deterministic_review": deterministic
    }
    payload_text = json.dumps(payload)

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload_text}
        ]
    )

    json_text = response.message.content
    review = json.loads(json_text)

    validate_review(review)

    return review


if __name__ == "__main__":
    report_path = Path("artifacts/irsim_benchmark_report.json")
    report_text = report_path.read_text(encoding="utf-8")
    report = json.loads(report_text)

    review = run_reviewer(report)

    output_path = Path("artifacts/benchmark_review.json")
    with output_path.open("w", encoding="utf-8") as file:
        json.dump(review, file, indent=2)

    print("Benchmark review saved")
    print(json.dumps(review, indent=2))