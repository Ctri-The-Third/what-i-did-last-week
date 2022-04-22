import logging
import math

from serviceHelpers.zendesk import zendesk, ZendeskTicket, ZendeskWorklog

from src.workItem import WorkItem
from src.common_methods import convert_min_to_time_str

_LO = logging.getLogger("zendeskWeeklog")
ZENDESK_CUSTOM_FIELD = 360028226411


class ZendeskWeeklog(zendesk):
    """Class to retrieve and instantiate a series of workitems from Zendesk"""

    def __init__(self, host: str, api_key, assignee):
        super().__init__(host, api_key)
        self.zen_assingee = assignee
        self.work_items = []
        self.logger = _LO

    def fetch_zendesk_tasks(self, last_week_date) -> list:
        "Trigger API calls to fetch tickets from zendesk and convert to work item"
        self.work_items = self._convert_zendesk_tasks_to_work_items(
            self._fetch_zendesk_tasks(last_week_date)
        )
        return self.work_items

    def _fetch_zendesk_tasks(self, last_week_date: str) -> dict:
        """Fetches ZD tasks

        `last_week_date` should be in the foromat %Y-%m-%d"""
        search_str = f"assignee:{self.zen_assingee} updated>={last_week_date}"
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
            time = convert_min_to_time_str(
                math.floor(self._get_time_total_for_task(ticket.id) / 60)
            )
            item = WorkItem("zendesk", f"ZD#{ticket.id} - {ticket.summary}", time)
            if ticket.status in ["solved", "closed"]:
                item.mark_complete()
            return_obj.append(item)
        return return_obj

    def _get_time_total_for_task(self, ticket_id) -> int:
        logs = self.get_worklogs(ticket_id, ZENDESK_CUSTOM_FIELD)
        total = 0
        for log in logs:
            log: ZendeskWorklog
            total += log.duration
        return total
