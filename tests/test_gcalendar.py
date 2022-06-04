import pytest
import os
import logging

from serviceHelpers.jira import JiraDetails, JiraTicket
from src.gcalendar_weeklog import (
    _convert_event_to_workitem,
    _get_duration_from_event,
    WorkItem,
    GCalendarWorklogger,
)
from src.common_methods import convert_jira_time_str_to_min


@pytest.mark.skip(reason="Requires interactive auth to test")
def test_init():
    pass


def test_event_parser():
    "check if the json handler crashes when bad things are sent"
    dicts = [
        {
            "kind": "calendar#event",
            "etag": '"3146010765518000"',
            "id": "21hnvro1tkjvsiuhgaije9csjr",
            "status": "cancelled",
        },
        {},
        123,
        "str",
        [],
        {
            "kind": "calendar#event",
            "etag": '"3206548994402000"',
            "id": "esbfsvbco8h0k2bmclrgebtjhr",
            "status": "confirmed",
            "htmlLink": "https://www.google.com/calendar/event?eid=value",
            "created": "2020-09-22T11:24:30.000Z",
            "updated": "2020-10-21T10:01:37.292Z",
            "summary": "Sample event",
            "creator": {"email": "sample@test.com", "self": True},
            "organizer": {"email": "sample@test.com", "self": True},
            "start": {
                "dateTime": "2020-10-22T12:30:00+01:00",
                "timeZone": "Europe/London",
            },
            "end": {
                "dateTime": "2020-10-22T14:00:00+01:00",
                "timeZone": "Europe/London",
            },
            "recurrence": ["RRULE:FREQ=WEEKLY;BYDAY=FR,MO,TH,TU,WE"],
            "iCalUID": "esbfsvbco8h0k2bmclrgebtjhr@google.com",
            "sequence": 2,
            "eventType": "default",
        },
    ]
    for di in dicts:
        _convert_event_to_workitem(di)


def test_duration_parser():
    "checks if the datetime parser is working"

    test = {
        "start": {"dateTime": "2020-10-22T12:30:00+01:00"},
        "end": {"dateTime": "2020-10-22T13:00:00+01:00"},
    }
    assert _get_duration_from_event(test) == 30

    test = {
        "start": {"dateTime": "2020-10-22T12:30:00Z"},
        "end": {"dateTime": "2020-10-22T13:00:00Z"},
    }
    assert _get_duration_from_event(test) == 30

    assert _get_duration_from_event({}) == 0

    assert _get_duration_from_event("str") == 0
