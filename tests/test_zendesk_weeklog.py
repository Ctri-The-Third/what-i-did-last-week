import os, re
from src.zendesk_weeklog import ZendeskWeekloger
from src.controller import Controller, _last_week_date

ZENDESK_CUSTOM_FIELD = 360028226411


def test_bad_zd_assignee():
    "with a bad assignee we should get an empty dict"
    zen = ZendeskWeekloger(
        os.environ["ZENDESK_HOST"],
        os.environ["ZENDESK_KEY"],
        "this_is_not_a_person@lies.com",
    )

    tickets = zen._fetch_zendesk_tasks(test_last_week_date())
    assert isinstance(tickets, dict)
    assert len(tickets) == 0


def test_last_week_date():
    "check the returned string matches the right format"

    date = _last_week_date(7)
    assert isinstance(date, str)
    match = re.match("[0-9]{4}-[0-2][0-9]-[0-3][0-9]", date)

    assert match is not None
    return date


def test_bad_zd_response():
    """Checks type handling of zd response"""
    zen = ZendeskWeekloger(
        os.environ["ZENDESK_HOST"], os.environ["ZENDESK_KEY"], "not_a_person@lies.com"
    )
    zen._convert_zendesk_tasks_to_work_items(["123", 456, None])
    bad_dict = {"Hello there": "hi!", 123: 456, "test3": None}
    zen._convert_zendesk_tasks_to_work_items(bad_dict)


def test_filter():
    """Checks whether or not the assignee is filtered properly"""

    zen = ZendeskWeekloger(
        os.environ["ZENDESK_HOST"], os.environ["ZENDESK_KEY"], os.environ["TEST_EMAIL"]
    )
    time = zen._get_time_total_for_task(1236377, "2022-05-17")
    assert time == 0
    time = zen._get_time_total_for_task(1236377, "2022-05-01")
    assert time == 1260
