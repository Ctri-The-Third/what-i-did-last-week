import sys


from dateutil.parser import parse
import math
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

from datetime import datetime, timedelta
import logging

from src.workItem import WorkItem

_TS_FORMAT = r"%Y-%m-%dT%H:%M:%S"
_LO = logging.getLogger("GCalendarWorklogger")


class GCalendarWorklogger:
    """Class to retrieve and instantiate a series of weeklogs based on google calendar events

    * `target` - an email address"""

    def __init__(self, creds: Credentials, target: str) -> None:
        self._creds = creds
        self._cal = build("calendar", "v3", credentials=creds)
        self._tar = target
        self.logger = _LO
        pass

    def fetch_calendar_tasks(self, target_date: str) -> list:
        "Retrieves events"
        work_items = {}
        try:
            # events = self._cal.events().list(calendarId="primary").execute()
            time_min = f"{target_date}T00:00:00Z"
            time_max = datetime.strftime(datetime.now(), _TS_FORMAT) + "Z"
            events = (
                self._cal.events()
                .list(calendarId="primary", timeMin=time_min, timeMax=time_max)
                .execute()
            )
        except Exception as err:
            self.logger.warning(err)

        for entry in events.get("items", []):
            if entry["status"] == "confirmed":
                if not _does_event_happen_within_bounds(entry, time_min, time_max):
                    continue

                item = work_items.get(
                    entry["summary"], _convert_event_to_workitem(entry)
                )

                item: WorkItem

                if "recurringEventId" not in entry and "recurrence" not in entry:
                    item.mark_complete()
                item.increase_time(_get_duration_from_event(entry))
                work_items[item.summary] = item

        return list(work_items.values())


def _does_event_happen_within_bounds(event: dict, time_min: str, time_max: str) -> bool:
    "checks if the event's start and finish times are within the boundaries provided"

    if "start" not in event:
        return False
    if "end" not in event:
        return False

    start = event["start"]
    end = event["end"]

    if "date" in start:
        start_ts = parse(start["date"])
        end_ts = parse(end["date"])
    elif "dateTime" in start:
        start_ts = parse(start["dateTime"])
        end_ts = parse(end["dateTime"])
    else:
        return False

    if start_ts < parse(time_min):
        return False
    if end_ts > parse(time_max):
        return False
    return True


def _convert_event_to_workitem(event: dict) -> WorkItem:
    "converts a json dict into a WorkItem"
    if not isinstance(event, dict):
        return None
    wi = return_object = WorkItem(
        "Calendar",
        event.get("summary", ""),
        "",
        event.get("id", ""),
        event.get("htmlLink", ""),
    )
    if wi.summary is None:
        return_object = None
    if wi.url is None:
        return_object = None
    return return_object


def _get_duration_from_event(event: dict) -> int:
    "returns the time in minutes that an event last"
    if not isinstance(event, dict):

        _LO.warning("value passed to duration parser is not a dict")
        return 0
    if "start" not in event:
        _LO.warning("duration parser missing 'start' object from passed dict ")
        return 0

    if "end" not in event:
        _LO.warning("duration parser missing 'end' object from passed dict ")
        return 0

    try:
        start = event["start"]["dateTime"]

        start_ts = parse(start)
        end = event["end"]["dateTime"]
        end_ts = parse(end)
        duration = end_ts - start_ts
    except Exception as err:
        return 0

    return math.floor(duration.seconds / 60)
