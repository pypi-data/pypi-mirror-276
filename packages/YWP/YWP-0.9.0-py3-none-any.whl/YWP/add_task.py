import json
from settings import *

def add_task(task_name, task_dis):
    tasks[task_name] = task_dis
    marks[task_name] = "no"
    with open(tasks_file, "w") as f:
        json.dump(tasks, f)
    with open(marks_file, "w") as f:
        json.dump(marks, f)
    return 'added'