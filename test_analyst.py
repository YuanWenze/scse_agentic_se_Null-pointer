import json
from pathlib import Path
from analyst_agent import run_analyst


def load_brief():
    brief_path = Path("brief.txt")
    text = brief_path.read_text(encoding="utf-8")
    return text

def save_requirements(requirements):
    artifacts_folder = Path("artifacts")
    artifacts_folder.mkdir(exist_ok=True)

    output_path = artifacts_folder / "requirements.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(requirements, file, indent=2)

def main():
    brief_text = load_brief()
    requirements = run_analyst(brief_text)

    if requirements is None:
        print("Analyst test failed")
    else:
        save_requirements(requirements)
        print("Analyst test passed")
        print(json.dumps(requirements, indent=2))

if __name__ == "__main__":
    main()