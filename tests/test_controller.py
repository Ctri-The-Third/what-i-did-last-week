from src.controller import Controller, WorkItem


def test_init():
    Controller()


def test_bad_zd_assignee():
    con = Controller()
    con.zen_assignee = "this_is_not_a_person@lies.com"
    tickets = con._fetch_zendesk_tasks()
    assert len(tickets) == 0


def test_bad_zd_response():
    con = Controller()
    con._convert_zendesk_tasks_to_work_items(["123", 456, None])
    bad_dict = {"Hello there": "hi!", 123: 456, "test3": None}
    con._convert_zendesk_tasks_to_work_items(bad_dict)


def test_generate_output():
    """Creates some fixed worklogs and compares their output"""
    con = Controller()

    source1s = ["I did one thing last week - but I finished it"]
    source2s = ["Did a little work on #a", "Task #123456 - thingy"]

    for source in source1s:
        log = WorkItem()
        log.done = True if source[0] in ["I"] else False
        log.summary = source
        log.source = "ITSM system"
        con.work_items.append(log)
    for source in source2s:
        log = WorkItem()
        log.done = True if source[0] in ["I"] else False
        log.summary = source
        log.source = "Jira"
        con.work_items.append(log)

    week_log = con.generate_weeklog()
    assert (
        week_log
        == "ITSM system\t🟢 - I did one thing last week - but I finished it\nJira\t🟡 - Did a little work on #a\nJira\t🟡 - Task #123456 - thingy\n"
    )
