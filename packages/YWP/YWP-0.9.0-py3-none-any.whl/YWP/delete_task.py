import json
from settings import *

def delete_task(task_name):
    if task_name in tasks:
        del tasks[task_name]
        del marks[task_name]
        with open(tasks_file, "w") as f:
            json.dump(tasks, f)
        with open(marks_file, "w") as f:
            json.dump(marks, f)
        return 'deleted'
    else:
        return 'not found'