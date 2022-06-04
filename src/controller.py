import os
from datetime import datetime, timedelta
import logging
from configparser import ConfigParser
from google.oauth2.credentials import Credentials


from serviceHelpers.models.JiraDetails import JiraDetails
from src.jira_weeklog import JiraWorklogger
from src.zendesk_weeklog import ZendeskWeekloger
from src.gcalendar_weeklog import GCalendarWorklogger
from src.freshdesk_weeklog import FreshdeskWeekloger


_LO = logging.getLogger("controller")


class Controller:
    """This controller class interacts with and initalises the service helpers to generate weeklogs.

    Expects the assginee to be an email address."""

    def __init__(
        self,
        assignee: str,
        google_creds: Credentials,
        how_many_days=7,
    ) -> None:
        self.assignee = assignee
        self.zen = ZendeskWeekloger(
            os.environ.get("ZENDESK_HOST"), os.environ.get("ZENDESK_KEY"), assignee
        )
        self.fresh = FreshdeskWeekloger(
            os.environ.get("FRESHDESK_HOST"), os.environ.get("FRESHDESK_KEY"), assignee
        )

        deets = JiraDetails()
        deets.host = os.environ.get("JIRA_HOST_1")
        deets.key = os.environ.get("JIRA_KEY_1")
        deets.name = "Jira_instance"
        self.jira = JiraWorklogger(deets, assignee)

        self.cal = GCalendarWorklogger(google_creds, assignee)
        lwd = datetime.now() - timedelta(how_many_days)
        lwd = lwd.replace(hour=0, minute=0, second=0)

        self.last_week_date = lwd.strftime(r"%Y-%m-%d")
        self.work_items = []
        self.logger = _LO

    def fetch_tasks(self) -> None:
        "Go through each enabled subservice and fetch work items from them"
        self.logger.info("Fetching Zendesk items")
        self.work_items += self.zen.fetch_zendesk_tasks(self.last_week_date)

        self.logger.info("Fetching Freshdesk items")
        self.work_items += self.fresh.fetch_freshdesk_tasks(self.last_week_date)

        self.logger.info("Fetching Jira items")
        self.work_items += self.jira.fetch_jira_tasks(self.last_week_date)

        self.logger.info("Trying to fetch Calendar items")
        self.work_items += self.cal.fetch_calendar_tasks(self.last_week_date)

    def generate_weeklog(self) -> str:
        """builds entries for each based on cached information"""
        out_str = ""
        for item in self.work_items:
            out_str += f"{item}\n"
        return out_str


def load_config() -> dict:
    "load the config"
    cfg = ConfigParser()
    cfg.read_file(open("last-week.cfg", "r", encoding="utf-8"))
    return cfg
