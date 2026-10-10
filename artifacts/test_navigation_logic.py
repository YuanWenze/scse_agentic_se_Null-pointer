import generated.navigation_logic as nav_logic

def test_forward_possible():
    state = {
        "goal_ahead": True,
        "front_blocked": False,
        "goal_on_left": False,
        "goal_on_right": False,
        "left_blocked": False,
        "right_blocked": False
    }
    assert nav_logic.decide_next_move(state) == "FORWARD"

def test_left_possible():
    state = {
        "goal_ahead": False,
        "front_blocked": True,
        "goal_on_left": True,
        "left_blocked": False,
        "goal_on_right": False,
        "right_blocked": False
    }
    assert nav_logic.decide_next_move(state) == "LEFT"

def test_right_possible():
    state = {
        "goal_ahead": False,
        "front_blocked": True,
        "goal_on_left": False,
        "goal_on_right": True,
        "left_blocked": False,
        "right_blocked": False
    }
    assert nav_logic.decide_next_move(state) == "RIGHT"

def test_all_blocked():
    state = {
        "goal_ahead": False,
        "front_blocked": True,
        "goal_on_left": False,
        "left_blocked": True,
        "goal_on_right": False,
        "right_blocked": True
    }
    assert nav_logic.decide_next_move(state) == "STOP"

def test_priority_left_over_forward():
    state = {
        "goal_ahead": True,
        "front_blocked": True,
        "goal_on_left": True,
        "left_blocked": False,
        "goal_on_right": False,
        "right_blocked": False
    }
    assert nav_logic.decide_next_move(state) == "LEFT"