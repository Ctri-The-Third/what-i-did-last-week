LARGEST_SOURCE = 0


class WorkItem:
    "represents a single piece of work done, and includes time worked"

    def __init__(self, source, summary, time_str: str = "", id="", url="") -> None:
        global LARGEST_SOURCE
        self.source = source
        LARGEST_SOURCE = max(len(source), LARGEST_SOURCE)
        self.done = False
        self.summary = summary
        self.time_str = time_str
        self.id = id
        self.url = ""

    def mark_complete(self):
        self.done = True

    def __str__(self):
        source_str = (self.source + (" " * (LARGEST_SOURCE + 1)))[0:LARGEST_SOURCE]
        summary_emoji = "🟢" if self.done == True else "🟡"
        time_str = (self.time_str + (" " * 8))[0:8]
        return f"{source_str} {summary_emoji} {time_str} - {self.summary}"
