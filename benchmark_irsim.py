import json
import subprocess

world_files = [
    "irsim_worlds/world_easy.yaml",
    "irsim_worlds/world_medium.yaml",
    "irsim_worlds/world_hard.yaml",
    "irsim_worlds/world_custom.yaml"
]


def run_world(world_file):
    subprocess.run(["python", "test_irsim_with_agent.py", world_file])

    report_path = "artifacts/irsim_report.json"
    with open(report_path, "r", encoding="utf-8") as file:
        report = json.load(file)

    return report


def main():
    results = []

    for world_file in world_files:
        print("Running:", world_file)
        report = run_world(world_file)
        report["world_file"] = world_file
        results.append(report)

    total = len(results)
    reached_goal_count = 0
    efficient_count = 0
    inefficient_success_count = 0
    failed_count = 0
    total_steps = 0

    for report in results:
        if report["reached_goal"]:
            reached_goal_count += 1

        status = report["efficiency_status"]
        if status == "efficient":
            efficient_count += 1
        elif status == "acceptable_but_inefficient":
            inefficient_success_count += 1
        else:
            failed_count += 1

        total_steps += report["steps_taken"]

    average_steps = total_steps / total

    benchmark_report = {
        "total_worlds": total,
        "goals_reached": reached_goal_count,
        "success_rate": reached_goal_count / total,
        "efficient_worlds": efficient_count,
        "inefficient_success_worlds": inefficient_success_count,
        "failed_worlds": failed_count,
        "efficiency_rate": efficient_count / total,
        "average_steps_taken": average_steps,
        "results": results
    }

    output_path = "artifacts/irsim_benchmark_report.json"
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(benchmark_report, file, indent=2)

    print("Benchmark report saved")
    print(json.dumps(benchmark_report, indent=2))


if __name__ == "__main__":
    main()