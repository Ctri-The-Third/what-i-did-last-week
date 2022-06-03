import os
import logging
from src.freshdesk_weeklog import FreshdeskWeekloger
from src.common_methods import convert_fd_time_str_to_min

FRESHDESK_KEY = os.environ.get("FRESHDESK_KEY")
FRESHDESK_HOST = os.environ.get("FRESHDESK_HOST")
TARGET_EMAIL = os.environ.get("TEST_EMAIL")


def test_env_host():
    "check the host is set"
    assert FRESHDESK_HOST


def test_env_key():
    "check the api key is set"
    assert FRESHDESK_KEY


def test_env_assignee():
    "check there's a target email"
    assert TARGET_EMAIL


def test_init(caplog):
    "checks the weeklog can init"
    _get_weeklog()

    no_warnings(caplog)


def test_time_str_converter():
    "check the time string converter doesn't break"
    assert convert_fd_time_str_to_min(0) == 0
    assert convert_fd_time_str_to_min("avacado") == 0
    assert convert_fd_time_str_to_min("123:456") == 0
    assert convert_fd_time_str_to_min("01:00") == 60
    assert convert_fd_time_str_to_min("01:30") == 90
    pass


def test_email_resolve(caplog):
    "check the user's email resolved to a user account"
    week = _get_weeklog()

    assert week.assignee_o.id is not None
    assert week.assignee_o.id > 0


def no_warnings(caplog):
    "asserts that there are no logs with the level number specified in the method"
    _no_records_with_level(caplog, logging.WARNING)


def _get_weeklog() -> FreshdeskWeekloger:
    return FreshdeskWeekloger(FRESHDESK_HOST, FRESHDESK_KEY, TARGET_EMAIL)


def _no_records_with_level(caplog, level):
    for record in caplog.records:
        assert record.levelno < level
