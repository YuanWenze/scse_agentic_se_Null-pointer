## the logic is similar to the run_planner and run_analyst files
import json
from pathlib import Path
from developer_agent import run_developer


## Create a function/logic that reads the plan from plan.json,
# then calls the run_developer function with the plan as input, and finally writes the validated code to code.json.
def load_plan():
    plan_path = Path("artifacts/plan.json")
    text = plan_path.read_text(encoding="utf-8")
    plan = json.loads(text)
    return plan


def save_code(code):
    artifacts_folder = Path("artifacts")
    artifacts_folder.mkdir(exist_ok=True)

    output_path = artifacts_folder / "code.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(code, file, indent=2)


def main():
    plan = load_plan()
    code = run_developer(plan)

    if code is None:
        print("Code validation failed")
    else:
        save_code(code)
        print("Code saved")
        print(json.dumps(code, indent=2))


if __name__ == "__main__":
    main()