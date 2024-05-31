import json
from settings import *

def load_tasks():

    with open (tasks_file, "w") as file:
        tasks = json.load(file)
    
    with open (marks_file, "w") as file:
        marks = json.load(file)

    return 'loaded'