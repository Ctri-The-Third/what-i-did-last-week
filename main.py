from src.controller import Controller, load_config
from src.workItem import WorkItem

if __name__ == "__main__":
    cfg = load_config("last-week.cfg")
    target = cfg.get("DEFAULT", "user_email")

    con = Controller(target)

    con.fetch_tasks()

    current_section = ""
    for log in con.work_items:
        log: WorkItem
        if log.source != current_section:
            print(f"--------------{log.source}-------------")
            current_section = log.source
        print(log)
