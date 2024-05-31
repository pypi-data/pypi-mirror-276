import json
import settings

def add_task(task_name, task_dis):
    tasks = settings.tasks()
    marks = settings.marks()
    tasks_file = settings.tasks_file()
    marks_file = settings.marks_file()

    tasks[task_name] = task_dis
    marks[task_name] = "no"
    with open(tasks_file, "w") as f:
        json.dump(tasks, f)
    with open(marks_file, "w") as f:
        json.dump(marks, f)

    settings.tasks = tasks
    settings.marks = marks

    return 'added'