## the logic is similar to the run_planner and run_analyst files
import json
from pathlib import Path
from planner_agent import run_planner

## Create a function/logic that reads the requirements from requirements.json, 
# then calls the run_planner function with the requirements as input, and finally writes the validated plan to plan.json.
def load_requirements():
    requirements_path = Path("artifacts/requirements.json")
    text = requirements_path.read_text(encoding="utf-8")
    requirements = json.loads(text)
    return requirements


def save_plan(plan):
    artifacts_folder = Path("artifacts")
    artifacts_folder.mkdir(exist_ok=True)

    output_path = artifacts_folder / "plan.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(plan, file, indent=2)


def main():
    requirements = load_requirements()
    plan = run_planner(requirements)

    if plan is None:
        print("Plan validation failed")
    else:
        save_plan(plan)
        print("Plan saved")
        print(json.dumps(plan, indent=2))


if __name__ == "__main__":
    main()