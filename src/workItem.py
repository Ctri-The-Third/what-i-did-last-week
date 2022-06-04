import math
import re

LARGEST_SOURCE = 0


class WorkItem:
    "represents a single piece of work done, and includes time worked"

    def __init__(self, source, summary, time_str: str = "0h 0m", id="", url="") -> None:
        global LARGEST_SOURCE
        self.source = source
        LARGEST_SOURCE = max(len(source), LARGEST_SOURCE)
        self.done = False
        self.summary = summary
        self.time_str = time_str
        self.time_mins = 0
        self.id = id
        self.url = url

    def mark_complete(self):
        self.done = True

    def __str__(self):
        source_str = (self.source + (" " * (LARGEST_SOURCE + 1)))[0:LARGEST_SOURCE]
        summary_emoji = "🟢" if self.done == True else "🟡"
        time_str = (self.time_str + (" " * 8))[0:8]
        return f"{source_str} {summary_emoji} {time_str} - {self.summary}"

    def increase_time(self, amount: int):
        "icnreases the amount of time in the event"
        if not isinstance(amount, int):
            return
        if self.time_mins == 0:
            self.time_mins == _convert_time_str_to_min(self.time_str)
        self.time_mins += amount
        self.time_str = _convert_min_to_time_str(self.time_mins)

    def __lt__(self, obj):
        return self.time_mins < obj.time_mins

    def __gt__(self, obj):
        return self.time_mins > obj.time_mins

    def __le__(self, obj):
        return self.time_mins <= obj.time_mins

    def __ge__(self, obj):
        return self.time_mins >= obj.time_mins

    def __eq__(self, obj):
        return self.time_mins == obj.time_mins


def _convert_min_to_time_str(mins: int) -> str:
    "Turn a number of minutes into a string in the format `1h 30m`"
    if not isinstance(mins, int):
        return "0h 0m"
    hours = math.floor(mins / 60)
    mins = mins % 60
    return f"{hours}h {mins}m"


def _convert_time_str_to_min(time_string: str) -> int:
    "Turn a time string back into a number of minutes"
    if not isinstance(time_string, str):

        return 0
    matches = re.match(r"([0-9])+h ([0-9])+m", time_string)
    if matches is None:
        return 0

    hours = int(matches[1])
    mins = int(matches[2])
    return hours * 60 + mins
