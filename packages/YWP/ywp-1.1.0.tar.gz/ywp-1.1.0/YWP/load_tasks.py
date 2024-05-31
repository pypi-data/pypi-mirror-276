import json
import settings

def load_tasks():
    tasks_file = settings.tasks_file()
    marks_file = settings.marks_file()

    with open (tasks_file, "w") as file:
        tasks = json.load(file)
    
    with open (marks_file, "w") as file:
        marks = json.load(file)

    settings.tasks = tasks
    settings.marks = marks

    return 'loaded'