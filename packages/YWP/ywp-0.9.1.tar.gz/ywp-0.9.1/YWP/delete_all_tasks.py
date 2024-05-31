import json
from settings import *

def delete_all_tasks():
    tasks = {}
    marks = {}

    with open (tasks_file, "w") as file:
        json.dump(tasks, file)
    
    with open (marks_file, "w") as file:
        json.dump(marks, file)

    return 'deleted'