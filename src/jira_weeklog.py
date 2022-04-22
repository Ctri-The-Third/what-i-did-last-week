import logging

from src.workItem import WorkItem
import re
import math
from serviceHelpers.jira import Jira, JiraTicket, JiraDetails


class JiraWorklog(Jira):
    """Class to retrieve and instantiate a series of workitems from Jira"""

    def __init__(self, config: JiraDetails, assignee) -> None:
        super().__init__(config)

        self.jira_assignee = assignee
        self.work_items = []
        self.logger = logging.getLogger("JiraWorklog")

    def fetch_jira_worklogs(self, target_date: str):
        "get a series of work items for the user"
        jql = f"assignee = {self.jira_assignee} AND updatedDate >= '{target_date}'"
        tickets = self.fetch_jira_tickets(jql)
