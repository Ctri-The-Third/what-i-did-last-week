import logging
from src.workItem import WorkItem
from serviceHelpers.freshdesk import FreshDesk, FreshdeskTicket

_LO = logging.getLogger("zendeskWeeklog")


class FreshdeskWeeklog(FreshDesk):
    def __init__(self, host, api_key, assignee) -> None:
        super().__init__(host, api_key)

        self.assignee = assignee

    def fetch_fd_tasks(self, last_week_date: str, assignee="") -> list:
        search_string = self.search_fd_tickets()
