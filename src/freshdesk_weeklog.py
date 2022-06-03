import logging
from serviceHelpers.freshdesk import FreshDesk, FreshdeskTicket

from src.workItem import WorkItem
from src.common_methods import convert_min_to_time_str
from src.common_methods import convert_fd_time_str_to_min


_LO = logging.getLogger("zendeskWeeklog")


class FreshdeskWeekloger(FreshDesk):
    """Class to retrieve and instantiate a series of workitems from Zendesk"""

    def __init__(self, host, api_key, assignee) -> None:
        super().__init__(host, api_key)
        self.assignee = assignee
        self.assignee_o = self.search_agent(email=assignee)
        self.work_items = []
        self.logger = _LO

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
                        and log.get("executed_at", "")[0:10] > last_week_date
                    ):
                        time_minutes += convert_fd_time_str_to_min(
                            log.get("time_spent", "00:00")
                        )
                time_str = convert_min_to_time_str(time_minutes)

                item = WorkItem(
                    "Freshdesk",
                    f"{ticket.subject}",
                    time_str,
                    f"FD#{ticket.id}",
                    f"https://{self.host}/a/tickets/{ticket.id}",
                )
                if ticket.status in [4, 5]:
                    item.mark_complete()
                self.work_items.append(item)
        return self.work_items
        # generate the contributions
