import json
import os
import subprocess
import sys

from analyst_agent import run_analyst
from planner_agent import run_planner
from developer_agent import run_developer, run_developer_revision
from reviewer_agent import run_reviewer
from reviewer_benchmark_agent import run_reviewer as run_benchmark_reviewer


def log(message):
    with open("trace.log", "a", encoding="utf-8") as file:
        file.write(message + "\n")
    print(message)


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def main():
    os.makedirs("artifacts", exist_ok=True)
    os.makedirs("generated", exist_ok=True)

    open("trace.log", "w").close()

    with open("brief.txt", "r", encoding="utf-8") as file:
        brief_text = file.read()
    log("Brief loaded")

    requirements = run_analyst(brief_text)
    save_json(requirements, "artifacts/requirements.json")
    log("Analyst Agent created requirements.json")

    plan = run_planner(requirements)
    save_json(plan, "artifacts/plan.json")
    log("Planner Agent created plan.json")

    code = run_developer(plan)
    with open("artifacts/navigation_logic.py", "w", encoding="utf-8") as file:
        file.write(code)
    with open("generated/navigation_logic.py", "w", encoding="utf-8") as file:
        file.write(code)
    log("Developer Agent created navigation_logic.py")

    subprocess.run([sys.executable, "runner.py"])
    log("Simulation Runner created simulation_report.json")

    simulation_report = load_json("artifacts/simulation_report.json")
    review = run_reviewer(simulation_report)
    save_json(review, "artifacts/review_report.json")
    log("Reviewer Agent created review_report.json")

    subprocess.run([sys.executable, "benchmark_irsim.py"])
    log("IR-SIM Benchmark created irsim_benchmark_report.json")

    benchmark_report = load_json("artifacts/irsim_benchmark_report.json")
    benchmark_review = run_benchmark_reviewer(benchmark_report)
    save_json(benchmark_review, "artifacts/benchmark_review.json")
    log("Benchmark Reviewer created benchmark_review.json")

    revised_code = run_developer_revision(
        code, review, benchmark_report, requirements, plan
    )

    if revised_code is not None:
        with open("generated/navigation_logic_v2.py", "w", encoding="utf-8") as file:
            file.write(revised_code)
        log("Developer Agent created navigation_logic_v2.py")


if __name__ == "__main__":
    main()