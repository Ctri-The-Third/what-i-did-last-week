from configparser import ConfigParser
from src.controller import Controller, WorkItem

if __name__ == "__main__":
    con = Controller()

    cfg = ConfigParser()
    cfg.read_file(open("last-week.cfg", "r", encoding="utf-8"))
    target = cfg.get("DEFAULT", "user_email")
    con.zen_assignee = target
    con.fetch_tasks()

    current_section = ""
    for log in con.work_items:
        log: WorkItem
        if log.source != current_section:
            print(f"--------------{log.source}-------------")
            current_section = log.source
        print(log)
