def decide_next_move(state):
    if state["front_blocked"]:
        if not state["left_blocked"]:
            return "LEFT"
        if not state["right_blocked"]:
            return "RIGHT"
        return "STOP"

    if state["goal_ahead"]:
        return "FORWARD"

    if state["goal_on_left"]:
        if not state["left_blocked"]:
            return "LEFT"
        if not state["front_blocked"]:
            return "FORWARD"
        if not state["right_blocked"]:
            return "RIGHT"
        return "STOP"

    if state["goal_on_right"]:
        if not state["right_blocked"]:
            return "RIGHT"
        if not state["front_blocked"]:
            return "FORWARD"
        if not state["left_blocked"]:
            return "LEFT"
        return "STOP"

    if not state["front_blocked"]:
        return "FORWARD"
    if not state["left_blocked"]:
        return "LEFT"
    if not state["right_blocked"]:
        return "RIGHT"
    return "STOP"