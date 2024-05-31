import json
import settings

def delete_all_tasks():
    tasks = {}
    marks = {}
    tasks_file = settings.tasks_file()
    marks_file = settings.marks_file()

    with open (tasks_file, "w") as file:
        json.dump(tasks, file)
    
    with open (marks_file, "w") as file:
        json.dump(marks, file)

    settings.tasks = tasks
    settings.marks = marks

    return 'deleted'