import json
from settings import *

def edit_mark_done_task(task_name, new_mark="yes"):
    if new_mark == "yes" or new_mark == "no":
        a = 0
    else:
        return 'not marked'
    if task_name in tasks:
        marks[task_name] = new_mark
        with open(marks_file, "w") as f:
            json.dump(marks, f)
        return 'marked'
    else:
        return 'not found'