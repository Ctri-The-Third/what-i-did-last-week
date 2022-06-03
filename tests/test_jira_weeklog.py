import os
import logging

from serviceHelpers.jira import JiraDetails, JiraTicket
from src.jira_weeklog import JiraWorklogger
from src.common_methods import convert_jira_time_str_to_min

JIRA_KEY = os.environ.get("JIRA_KEY_1")
JIRA_HOST = os.environ.get("JIRA_HOST_1")
TARGET_EMAIL = os.environ.get("TEST_EMAIL")


def test_keys():
    assert JIRA_KEY


def test_host():
    assert JIRA_HOST


def test_email():
    assert TARGET_EMAIL


def test_init() -> JiraWorklogger:

    deets = JiraDetails()
    deets.host = JIRA_HOST
    deets.key = JIRA_KEY
    jira = JiraWorklogger(deets, TARGET_EMAIL)
    return jira


def test_ticket_fetch():

    jira = test_init()
    tickets = jira.fetch_jira_tickets("key = GSDSE-51")
    assert len(tickets) == 1

    for ticket_key in tickets:
        ticket = tickets[ticket_key]
        assert isinstance(ticket, JiraTicket)
        assert isinstance(ticket_key, str)
