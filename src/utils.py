# utils.py

def add_task(tasks, title, due_date=None, priority=1):
    if not title:
        raise ValueError("Title is required")
    task = {
        "title": title,
        "due_date": due_date,
        "priority": priority,
        "completed": False
    }
    tasks.append(task)
    return tasks

def complete_task(tasks, index):
    if index < 0 or index >= len(tasks):
        raise IndexError("Invalid task index")
    tasks[index]["completed"] = True
    return tasks
