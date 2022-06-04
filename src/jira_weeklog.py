import logging
from serviceHelpers.jira import Jira, JiraTicket, JiraDetails, JiraWorklog
import math
from src.workItem import WorkItem
from src.common_methods import convert_min_to_time_str


class JiraWorklogger(Jira):
    """Class to retrieve and instantiate a series of workitems from Jira"""

    def __init__(self, config: JiraDetails, assignee) -> None:
        super().__init__(config)

        self.jira_assignee = assignee
        self.work_items = []
        self.logger = logging.getLogger("JiraWorklog")

    def fetch_jira_tasks(self, target_date: str):
        "get a series of work items for the user"
        self.jira_assignee: str
        assignee = self.jira_assignee.replace("@", "\u0040")
        jql = f"assignee = '{assignee}' AND updatedDate >= '{target_date}'"
        tickets = self.fetch_jira_tickets(jql)
        workitems = []
        for ticket_id in tickets:
            ticket: JiraTicket = tickets[ticket_id]
            if (
                ticket.assignee_id != self.jira_assignee
                and ticket.assignee_email != self.jira_assignee
            ):
                continue

            item = WorkItem(
                "Jira",
                ticket.summary,
                "",
                ticket.key,
                f"https://{self.host}/browse/{ticket.key}",
            )
            all_logs = self.fetch_worklogs_for_jira_ticket(ticket.key)
            if ticket.status in ["Done", "Resolved", "Closed"]:
                item.mark_complete()

            seconds = 0
            for log in all_logs:
                log: JiraWorklog
                # self.logger.debug(log.author_email, log.duration_seconds)
                if (
                    self.jira_assignee in [log.author_email, log.author_key]
                    and log.created.strftime(r"%Y-%m-%d") >= target_date
                ):
                    seconds += log.duration_seconds
            item.increase_time(math.floor(seconds / 60))

            workitems.append(item)

        return workitems
