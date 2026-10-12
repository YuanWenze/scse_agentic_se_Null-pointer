import json
from pathlib import Path
from generated.navigation_logic import decide_next_move


def run_simulation():
    scenarios = [
        (
            {
                "goal_ahead": True,
                "goal_on_left": False,
                "goal_on_right": False,
                "front_blocked": False,
                "left_blocked": False,
                "right_blocked": False
            },
            "FORWARD"
        ),
        (
            {
                "goal_ahead": False,
                "goal_on_left": True,
                "goal_on_right": False,
                "front_blocked": False,
                "left_blocked": False,
                "right_blocked": False
            },
            "LEFT"
        ),
        (
            {
                "goal_ahead": False,
                "goal_on_left": False,
                "goal_on_right": True,
                "front_blocked": False,
                "left_blocked": False,
                "right_blocked": False
            },
            "RIGHT"
        ),
        (
            {
                "goal_ahead": False,
                "goal_on_left": False,
                "goal_on_right": False,
                "front_blocked": False,
                "left_blocked": False,
                "right_blocked": False
            },
            "FORWARD"
        ),
        (
            {
                "goal_ahead": True,
                "goal_on_left": False,
                "goal_on_right": False,
                "front_blocked": True,
                "left_blocked": True,
                "right_blocked": True
            },
            "STOP"
        ),
        (
            {
                "goal_ahead": True,
                "goal_on_left": False,
                "goal_on_right": False,
                "front_blocked": True,
                "left_blocked": False,
                "right_blocked": False
            },
            "LEFT"
        ),
        (
            {
                "goal_ahead": False,
                "goal_on_left": False,
                "goal_on_right": True,
                "front_blocked": False,
                "left_blocked": False,
                "right_blocked": True
            },
            "FORWARD"
        )
    ]

    results = []
    passed = 0
    failed = 0

    for state, expected in scenarios:
        actual = decide_next_move(state)
        if actual == expected:
            passed += 1
            ok = True
        else:
            failed += 1
            ok = False

        results.append({
            "state": state,
            "expected": expected,
            "actual": actual,
            "passed": ok
        })

    total = len(scenarios)

    report = {
        "total_scenarios": total,
        "passed": passed,
        "failed": failed,
        "success_rate": passed / total,
        "results": results
    }

    return report


if __name__ == "__main__":
    report = run_simulation()

    output_folder = Path("artifacts")
    output_folder.mkdir(exist_ok=True)
    output_path = output_folder / "simulation_report.json"

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("Simulation report saved")
    print(json.dumps(report, indent=2))
