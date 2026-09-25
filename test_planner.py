import json
from pathlib import Path
from planner_agent import run_planner

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
        print("Planner test failed")
    else:
        save_plan(plan)
        print("Planner test passed")
        print(json.dumps(plan, indent=2))

if __name__ == "__main__":
    main()