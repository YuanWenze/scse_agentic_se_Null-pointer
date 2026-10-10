import json
from pathlib import Path
from ollama import chat

system_prompt = """
You are a test agent for a mobile robot.
Read the requirements and the plan in JSON format.
Generate pytest-style Python test code for the function decide_next_move(state).
Output ONLY the Python code. Do not write anything else.

The state parameter is a dictionary with these keys:
"goal_ahead", "goal_on_left", "goal_on_right",
"front_blocked", "left_blocked", "right_blocked"

The function returns one of: "FORWARD", "LEFT", "RIGHT", "STOP".

The test code must:
- import decide_next_move from generated.navigation_logic
- define at least 5 test functions
- use assert statements
"""


def validate_test_code(code):
    if not isinstance(code, str):
        return False

    if len(code) == 0:
        return False

    if "```" in code:
        return False

    if "import" not in code:
        return False
    if "assert" not in code:
        return False
    if "decide_next_move" not in code:
        return False

    return True


def run_test_agent(requirements, plan):
    payload = {
        "requirements": requirements,
        "plan": plan
    }
    payload_text = json.dumps(payload)

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": payload_text}
        ]
    )

    code = response.message.content

    if validate_test_code(code):
        return code
    else:
        return None


if __name__ == "__main__":
    requirements_path = Path("artifacts/requirements.json")
    plan_path = Path("artifacts/plan.json")

    requirements = json.loads(requirements_path.read_text(encoding="utf-8"))
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    code = run_test_agent(requirements, plan)

    if code is None:
        print("Test code validation failed")
    else:
        output_path = Path("artifacts/test_navigation_logic.py")
        output_path.write_text(code, encoding="utf-8")

        print("Test code saved")
        print(code)