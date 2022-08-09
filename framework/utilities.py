import re


weekdays = ("Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday")


def parse_timer_text(name: str) -> str:
    time = [0] * 3
    patterns = [re.compile(r"(\d+) hours"), re.compile(r"(\d+) minutes"), re.compile(r"(\d+) seconds")]

    for i in range(3):
        match = patterns[i].search(name)
        if match:
            time[i] = int(match.group(1))

    return ":".join(f"{x:02}" for x in time)


def parse_stopwatch_text(name: str) -> str:
    centiseconds = 0

    match = re.search(r"(\d+) centiseconds", name)
    if match:
        centiseconds = int(match.group(1))

    return parse_timer_text(name) + f".{centiseconds:02}"
