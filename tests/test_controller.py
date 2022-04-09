from src.controller import Controller
from src.workItem import WorkItem


def test_init():

    Controller("test@test.com")


def test_generate_output():
    """Creates some fixed worklogs and compares their output"""
    con = Controller("test@test.com")

    source1s = ["I did one thing last week - but I finished it"]
    source2s = ["Did a little work on #a", "Task #123456 - thingy"]

    for source in source1s:
        log = WorkItem("ITSM system", source)
        log.done = True if source[0] in ["I"] else False

        con.work_items.append(log)
    for source in source2s:
        log = WorkItem("Jira", source)
        log.done = True if source[0] in ["I"] else False
        con.work_items.append(log)

    week_log = con.generate_weeklog()
    assert (
        week_log
        == "ITSM system\t🟢 - I did one thing last week - but I finished it\nJira\t🟡 - Did a little work on #a\nJira\t🟡 - Task #123456 - thingy\n"
    )
