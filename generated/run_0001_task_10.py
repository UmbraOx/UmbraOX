def play_game(level):
    if level < 1:
        raise ValueError("Level must be at least 1")
    return f"Playing on level {level}"

def end_game():
    return "Game ended"
