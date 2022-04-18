import os
from datetime import datetime, timedelta
import logging
from configparser import ConfigParser

from src.zendesk_weeklog import ZendeskWeeklog

_LO = logging.getLogger("controller")


class Controller:
    """This controller class interacts with and initalises the hex helpers to generate weeklogs"""

    def __init__(self, assignee: str) -> None:
        self.assignee = assignee
        self.zen = ZendeskWeeklog(
            os.environ.get("ZENDESK_HOST"), os.environ.get("ZENDESK_KEY"), assignee
        )
        lwd = datetime.now() - timedelta(days=7)
        lwd = lwd.replace(hour=0, minute=0, second=0)
        self.last_week_date = lwd.strftime(r"%Y-%m-%d")
        self.work_items = []

    def fetch_tasks(self) -> None:
        "Go through each enabled subservice and fetch work items from them"
        self.work_items |= self.zen.fetch_zendesk_tasks(self.last_week_date)

    def generate_weeklog(self) -> str:
        """builds entries for each based on cached information"""
        out_str = ""
        for item in self.work_items:
            out_str += f"{item}\n"
        return out_str


def load_config(path="last-week.cfg") -> ConfigParser:
    "loads a config file and returns the un-vetted content"
    cfg = ConfigParser()
    cfg.read_file(open(path, "r", encoding="utf-8"))
    return cfg
