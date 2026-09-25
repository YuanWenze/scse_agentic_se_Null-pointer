## A typical test case: 
""" {
    "goal_ahead": True,
    "goal_on_left": False,
    "goal_on_right": False,
    "front_blocked": False,
    "left_blocked": False,
    "right_blocked": False
},
"FORWARD" """
## Use the above test case to create more test cases for all the possible states
from artifacts.navigation_logic import decide_next_move
def run_tests():
    test_cases = [
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
            "STOP"
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
    ]
    for state, expected in test_cases:
        result = decide_next_move(state)
        if result == expected:
            print("PASS")
        else:
            print("FAIL: expected", expected, "but got", result)
if __name__ == "__main__":
    run_tests()