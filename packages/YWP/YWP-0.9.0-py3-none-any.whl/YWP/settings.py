import os
import json

setting_file = "settings.json"
tasks_file = "tasks.json"
marks_file = "marks.json"
tasks = {}
marks = {}

if os.path.exists(tasks_file):
    with open(tasks_file, "r") as f:
        tasks = json.load(f)

if os.path.exists(marks_file):
    with open(marks_file, "r") as f:
        marks = json.load(f)