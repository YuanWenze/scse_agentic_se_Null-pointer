import json
from ollama import chat

system_prompt = """
You are a developer agent for a mobile robot.
Read the navigation plan in JSON format.
Generate Python code for a function called decide_next_move(state).
Output ONLY the Python code. Do not write anything else.

The state parameter is a dictionary with these keys:
"goal_ahead": True or False
"goal_on_left": True or False
"goal_on_right": True or False
"front_blocked": True or False
"left_blocked": True or False
"right_blocked": True or False

The function must return exactly one of: "FORWARD", "LEFT", "RIGHT", "STOP".

Example of correct output:
def decide_next_move(state):
    if state["goal_ahead"] and not state["front_blocked"]:
        return "FORWARD"
    if state["goal_on_left"] and not state["left_blocked"]:
        return "LEFT"
    if state["goal_on_right"] and not state["right_blocked"]:
        return "RIGHT"
    return "STOP"
"""


def validate_code(code):
    if not isinstance(code, str):
        return False

    if "def decide_next_move(state):" not in code:
        return False

    return True


def run_developer(plan):
    plan_text = json.dumps(plan)

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": plan_text}
        ]
    )

    code = response.message.content

    if validate_code(code):
        return code
    else:
        return None


def run_developer_revision(original_code, review_notes, benchmark_report, requirements, plan):
    revision_system_prompt = """
You are a developer agent for a mobile robot.
You will receive the original navigation code, review notes, benchmark report, requirements and plan.
Generate a revised version of the decide_next_move(state) function.
Output ONLY the Python code. Do not write anything else.

The state parameter has these keys:
"goal_ahead", "goal_on_left", "goal_on_right",
"front_blocked", "left_blocked", "right_blocked"

The function must return exactly one of: "FORWARD", "LEFT", "RIGHT", "STOP".
"""

    payload = {
        "original_code": original_code,
        "review_notes": review_notes,
        "benchmark_report": benchmark_report,
        "requirements": requirements,
        "plan": plan
    }
    payload_text = json.dumps(payload)

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": revision_system_prompt},
            {"role": "user", "content": payload_text}
        ]
    )

    code = response.message.content

    if validate_code(code):
        return code
    else:
        return None