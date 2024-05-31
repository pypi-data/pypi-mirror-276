import json
import settings

def edit_task(task_name, new_task_dis):
    tasks = settings.tasks()
    marks = settings.marks()
    tasks_file = settings.tasks_file()
    marks_file = settings.marks_file()

    if task_name in tasks:
        tasks[task_name] = new_task_dis
        with open(tasks_file, "w") as f:
            json.dump(tasks, f)

        settings.tasks = tasks
        settings.marks = marks

        return 'edited'
    else:
        return 'not_found'