import json
from ollama import chat


def validate_requirements(data):
    if not isinstance(data, dict):
        return False

    keys = ["goal", "allowed_actions", "safe_stop", "avoid_obstacles"]
    for key in keys:
        if key not in data:
            return False

    if len(data) != 4:
        return False

    if not isinstance(data["goal"], str):
        return False
    if not isinstance(data["allowed_actions"], list):
        return False
    if not isinstance(data["safe_stop"], bool):
        return False
    if not isinstance(data["avoid_obstacles"], bool):
        return False

    for action in data["allowed_actions"]:
        if action not in ["FORWARD", "LEFT", "RIGHT", "STOP"]:
            return False

    return True

def run_analyst(brief_text):
    system_prompt = """
You are a software requirements analyst.
Read the robot navigation brief.
Output ONLY a valid JSON object.
Do not write anything else.

The JSON must have exactly these keys:
"goal": a string. Write the actual navigation objective you understood from the brief. Do NOT write the word "goal".
"allowed_actions": a list containing only FORWARD, LEFT, RIGHT, STOP
"safe_stop": true or false
"avoid_obstacles": true or false

Example of correct output:
{
  "goal": "Move toward the goal position",
  "allowed_actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
  "safe_stop": true,
  "avoid_obstacles": true
}
"""

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": brief_text}
        ]
    )

    json_text = response.message.content
    requirements = json.loads(json_text)

    if validate_requirements(requirements):
        return requirements
    else:
        return None