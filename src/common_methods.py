import re
import math


def convert_time_str_to_min(time_string: str) -> int:
    if not isinstance(time_string, str):

        return 0
    if re.match(r"[0-9]{2}:[0-9]{2}", time_string) is None:
        return 0

    hours = int(time_string[0:2])
    mins = int(time_string[3:5])
    return hours * 60 + mins


def convert_min_to_time_str(mins: int) -> str:
    if not isinstance(mins, int):
        return "0h 0m"
    hours = math.floor(mins / 60)
    mins = mins % 60
    return f"{hours}h {mins}m"
