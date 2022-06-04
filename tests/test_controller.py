import pytest
from src.controller import Controller
from src.workItem import WorkItem


@pytest.mark.skip(reason="This now requires google credentials to execute.")
def test_init():
    "check the controller initialises"
    con = Controller("test@test.com", None)


@pytest.mark.skip(reason="This now requires google credentials to execute.")
def test_generate_output():
    """Creates some fixed worklogs and compares their output"""
    con = Controller("test@test.com", None)

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
        == "ITSM system 🟢          - I did one thing last week - but I finished it\nJira        🟡          - Did a little work on #a\nJira        🟡          - Task #123456 - thingy\n"
    )


def test_files_present():
    open("src/intro_page.md", "r+")
    open("src/output_page.md", "r+")
