from src.workItem import *


def test_default_init():
    item = WorkItem("source", "summary")
    assert item.source == "source"
    assert item.summary == "summary"
    assert item.time_str == "0h 0m"
    assert item.id == ""
    assert item.url == ""
    assert item.done is False


def test_complete():
    item = WorkItem("source", "summary")
    assert item.done is False

    item.mark_complete()
    assert item.done


def test_increase():
    item = WorkItem("source", "summary")

    assert item.time_mins == 0
    assert item.time_str == "0h 0m"
    item.increase_time(5)
    assert item.time_mins == 5
    assert item.time_str == "0h 5m"

    item.increase_time(60)
    assert item.time_mins == 65
    assert item.time_str == "1h 5m"

    item.increase_time("hello")
    assert item.time_mins == 65
