import os
from datetime import datetime, timedelta
import logging
from serviceHelpers.zendesk import zendesk, ZendeskTicket

_LO = logging.getLogger("controller")


class Controller:
    """This controller class interacts with and initalises the service helpers to generate weeklogs"""

    def __init__(self) -> None:

        self.zen = zendesk(
            os.environ.get("ZENDESK_HOST"), os.environ.get("ZENDESK_KEY")
        )
        lwd = datetime.now() - timedelta(days=7)
        lwd = lwd.replace(hour=0, minute=0, second=0)
        self.last_week_date = lwd.strftime(r"%Y-%m-%d")
        self.zen_assignee = "zd_username"

        self.work_items = []

    def fetch_tasks(self) -> None:
        self._convert_zendesk_tasks_to_work_items(self._fetch_zendesk_tasks())

    def generate_weeklog(self) -> str:
        """builds entries for each based on cached information"""
        out_str = ""
        for item in self.work_items:
            out_str += f"{item}\n"
        return out_str

    def _fetch_zendesk_tasks(self) -> dict:
        """Fetches ZD tasks"""
        search_str = f"assignee:{self.zen_assignee} updated>={self.last_week_date}"
        zd_tickets = self.zen.search_for_tickets(search_str)
        return zd_tickets

    def _convert_zendesk_tasks_to_work_items(self, zd_tickets: dict) -> None:
        """takes fetched ZD tickets and applies them to"""

        if not isinstance(zd_tickets, dict):
            _LO.warning("Expected dict input from `_fetch_zendesk_tickets`, aborting")
            return
        for key in zd_tickets:
            if not isinstance(key, str):
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

            item = WorkItem("zendesk", ticket.summary)
            if ticket.status in ["solved", "closed"]:
                item.mark_complete()
            self.work_items.append(item)


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
