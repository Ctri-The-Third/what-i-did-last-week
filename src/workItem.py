class WorkItem:
    def __init__(self, source, summary) -> None:
        self.source = source
        self.done = False
        self.summary = summary

    def mark_complete(self):
        self.done = True

    def __str__(self):
        summary_emoji = "🟢" if self.done == True else "🟡"
        return f"{self.source}\t{summary_emoji} - {self.summary}"
