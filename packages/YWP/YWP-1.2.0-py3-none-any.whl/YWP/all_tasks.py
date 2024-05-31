import json
import settings
import load_tasks

def all_tasks():
    load_tasks.load_tasks()
    tasks = settings.tasks()
    marks = settings.marks()

    return {"tasks": tasks, "marks": marks}