# Reference: https://www.python.ambitious-engineer.com/archives/3721
def colorize(text, color_code):
    return f"\033[{color_code}m{text}\033[0m"