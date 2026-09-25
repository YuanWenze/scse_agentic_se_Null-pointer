## test_developer.py
## Read artifacts/plan.json, send it to the developer agent, and save the result to artifacts/navigation_logic.py.

import json
from pathlib import Path
from developer_agent import run_developer

def load_plan():
    plan_path = Path("artifacts/plan.json")
    text = plan_path.read_text(encoding="utf-8")
    plan = json.loads(text)
    return plan

def save_code(code):
    artifacts_folder = Path("artifacts")
    artifacts_folder.mkdir(exist_ok=True)

    output_path = artifacts_folder / "navigation_logic.py"

    with output_path.open("w", encoding="utf-8") as file:
        file.write(code)

def main():
    plan = load_plan()
    code = run_developer(plan)

    if code is None:
        print("Developer test failed")
    else:
        save_code(code)
        print("Developer test passed")
        print(code)

if __name__ == "__main__":
    main()