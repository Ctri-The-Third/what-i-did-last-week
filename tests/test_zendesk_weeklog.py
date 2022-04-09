import os, re
from src.zendeskWeeklog import ZendeskWeeklog
from src.controller import Controller


def test_bad_zd_assignee():
    "with a bad assignee we should get an empty dict"
    zen = ZendeskWeeklog(
        os.environ["ZENDESK_HOST"],
        os.environ["ZENDESK_KEY"],
        "this_is_not_a_person@lies.com",
    )

    tickets = zen._fetch_zendesk_tasks(test_last_week_date())
    assert isinstance(tickets, dict)
    assert len(tickets) == 0


def test_last_week_date():
    "check the returned string matches the right format"

    date = Controller("test@test.com").last_week_date
    assert isinstance(date, str)
    match = re.match("[0-9]{4}-[0-2][0-9]-[0-3][0-9]", date)

    assert match is not None
    return date


def test_bad_zd_response():
    """Checks type handling of zd response"""
    zen = ZendeskWeeklog(
        os.environ["ZENDESK_HOST"],
        os.environ["ZENDESK_KEY"],
        "sebastiano.todaro@unity3d.com",
    )
    zen._convert_zendesk_tasks_to_work_items(["123", 456, None])
    bad_dict = {"Hello there": "hi!", 123: 456, "test3": None}
    zen._convert_zendesk_tasks_to_work_items(bad_dict)
