import json
from settings import *

def edit_task(task_name, new_task_dis):
    if task_name in tasks:
        tasks[task_name] = new_task_dis
        with open(tasks_file, "w") as f:
            json.dump(tasks, f)
        return 'edited'
    else:
        return 'not_found'