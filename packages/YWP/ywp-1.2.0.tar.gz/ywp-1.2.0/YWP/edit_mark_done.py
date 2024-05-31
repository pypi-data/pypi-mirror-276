import json
import settings

def task_mark_done(task_name, new_mark="yes"):
    tasks = settings.tasks()
    marks = settings.marks()
    tasks_file = settings.tasks_file()
    marks_file = settings.marks_file()

    if new_mark == "yes" or new_mark == "no":
        a = 0
    else:
        return 'not marked'
    if task_name in tasks:
        marks[task_name] = new_mark
        with open(marks_file, "w") as f:
            json.dump(marks, f)

        settings.tasks = tasks
        settings.marks = marks
        
        return 'marked'
    else:
        return 'not found'