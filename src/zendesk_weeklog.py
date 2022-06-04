import logging
import math

from serviceHelpers.zendesk import zendesk, ZendeskTicket, ZendeskWorklog, ZendeskUser

from src.workItem import WorkItem
from src.common_methods import convert_min_to_time_str

_LO = logging.getLogger("zendeskWeeklog")
ZENDESK_CUSTOM_FIELD = 360028226411


class ZendeskWeekloger(zendesk):
    """Class to retrieve and instantiate a series of workitems from Zendesk"""

    def __init__(self, host: str, api_key, assignee):
        super().__init__(host, api_key)

        if host is None or api_key is None:
            _LO.warning("Didn't init with host, or API key. Check environs.")
        self.work_items = []
        self.logger = _LO
        self.zen_assignee = ZendeskUser({})
        for obj in self.search_for_users(assignee).values():
            obj: ZendeskUser
            self.zen_assignee = obj if obj.email == assignee else self.zen_assignee
        self.target_date_str = ""

    def fetch_zendesk_tasks(self, last_week_date) -> list:
        "Trigger API calls to fetch tickets from zendesk and convert to work item"

        self.target_date_str = last_week_date

        self.work_items = self._convert_zendesk_tasks_to_work_items(
            self._fetch_zendesk_tasks(last_week_date)
        )
        return self.work_items

    def _fetch_zendesk_tasks(self, last_week_date: str) -> dict:
        """Fetches ZD tasks

        `last_week_date` should be in the foromat %Y-%m-%d"""
        search_str = f"assignee:{self.zen_assignee.user_id} updated>={last_week_date}"
        zd_tickets = self.search_for_tickets(search_str)
        return zd_tickets

    def _convert_zendesk_tasks_to_work_items(self, zd_tickets: dict) -> None:
        """takes fetched ZD tickets and applies them to"""

        if not isinstance(zd_tickets, dict):
            _LO.warning("Expected dict input from `_fetch_zendesk_tickets`, aborting")
            return

        return_obj = []
        for key in zd_tickets:
            if not isinstance(key, int):
                _LO.warning("Discarding weird zendesk ticket response key: %s", key)
                continue
            ticket: ZendeskTicket = zd_tickets[key]
            if not isinstance(ticket, ZendeskTicket):
                _LO.warning(
                    "Discarding weird zendesk ticket response content: %s-%s",
                    key,
                    ticket,
                )

                continue
            time = math.floor(
                self._get_time_total_for_task(ticket.id, self.target_date_str) / 60
            )
            item = WorkItem(
                "zendesk",
                ticket.summary,
                "",
                f"ZD#{ticket.id}",
                url=f"https://{self.host}/agent/tickets/{ticket.id}",
            )
            item.increase_time(time)
            if ticket.status in ["solved", "closed"]:
                item.mark_complete()
            return_obj.append(item)
        return return_obj

    def _get_time_total_for_task(self, ticket_id, target_date_str) -> int:

        logs = self.get_worklogs(ticket_id, ZENDESK_CUSTOM_FIELD)
        total = 0
        for log in logs:
            log: ZendeskWorklog
            if log.author_id != self.zen_assignee.user_id:
                continue
            if log.timestamp.strftime(r"%Y-%m-%d") < target_date_str:
                continue
            total += log.duration
        return total
