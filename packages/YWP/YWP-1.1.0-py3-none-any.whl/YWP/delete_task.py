import json
import settings

def delete_task(task_name):
    tasks = settings.tasks()
    marks = settings.marks()
    tasks_file = settings.tasks_file()
    marks_file = settings.marks_file()

    if task_name in tasks:
        del tasks[task_name]
        del marks[task_name]
        with open(tasks_file, "w") as f:
            json.dump(tasks, f)
        with open(marks_file, "w") as f:
            json.dump(marks, f)

        settings.tasks = tasks
        settings.marks = marks

        return 'deleted'
    else:
        return 'not found'