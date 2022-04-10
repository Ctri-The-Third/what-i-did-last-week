import logging

from src.workItem import WorkItem
import re
import math
from serviceHelpers.freshdesk import FreshDesk, FreshdeskTicket

_LO = logging.getLogger("zendeskWeeklog")


class FreshdeskWeeklog(FreshDesk):
    """Class to retrieve and instantiate a series of workitems from Zendesk"""

    def __init__(self, host, api_key, assignee) -> None:
        super().__init__(host, api_key)
        self.assignee = assignee
        self.assignee_o = self.search_agent(email=assignee)
        self.work_items = []

    def fetch_freshdesk_tasks(self, last_week_date: str) -> list:
        "Trigger API calls to fetch tickets from zendesk and convert to work item"

        query_string = (
            f"updated_at:>'{last_week_date}' AND agent_id:{self.assignee_o.id}"
        )
        tickets = self.search_fd_tickets(query_string)
        # generate the big work items (assigned tickets)
        for ticket_key in tickets:
            ticket: FreshdeskTicket = tickets[ticket_key]
            if ticket.responder_id == self.assignee_o.id:

                worklogs = self.get_worklogs(ticket_key)
                time_minutes = 0
                for log in worklogs:
                    if (
                        log.get("agent_id", 0) == self.assignee_o.id
                        and log.get("executed_at"[0:10], "") > last_week_date
                    ):
                        time_minutes += _convert_time_str_to_min(
                            log.get("time_spent", "00:00")
                        )
                time_str = _convert_min_to_time_str(time_minutes)

                item = WorkItem(
                    "Freshdesk", f"FD#{ticket.id} - {ticket.subject}", time_str
                )
                if ticket.status in [4, 5]:
                    item.mark_complete()
                self.work_items.append(item)
        return self.work_items
        # generate the contributions


def _convert_time_str_to_min(time_string: str) -> int:
    if not isinstance(time_string, str):

        return 0
    if re.match(r"[0-9]{2}:[0-9]{2}", time_string) is None:
        return 0

    hours = int(time_string[0:2])
    mins = int(time_string[3:5])
    return hours * 60 + mins


def _convert_min_to_time_str(mins: int) -> str:
    if not isinstance(mins, int):
        return "0h 0m"
    hours = math.floor(mins / 60)
    mins = mins % 60
    return f"{hours}h {mins}m"
