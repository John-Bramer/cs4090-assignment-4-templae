import json
import os
from datetime import datetime, timedelta

# File path for task storage
DEFAULT_TASKS_FILE = "tasks.json"

def load_tasks(file_path=DEFAULT_TASKS_FILE):
    """
    Load tasks from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file containing tasks
        
    Returns:
        list: List of task dictionaries, empty list if file doesn't exist
    """
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        # Handle corrupted JSON file
        print(f"Warning: {file_path} contains invalid JSON. Creating new tasks list.")
        return []

def save_tasks(tasks, file_path=DEFAULT_TASKS_FILE):
    """
    Save tasks to a JSON file.
    
    Args:
        tasks (list): List of task dictionaries
        file_path (str): Path to save the JSON file
    """
    with open(file_path, "w") as f:
        json.dump(tasks, f, indent=2)

def generate_unique_id(tasks):
    """
    Generate a unique ID for a new task.
    
    Args:
        tasks (list): List of existing task dictionaries
        
    Returns:
        int: A unique ID for a new task
    """
    if not tasks:
        return 1
    return max(task["id"] for task in tasks) + 1

def filter_tasks_by_priority(tasks, priority):
    """
    Filter tasks by priority level.
    
    Args:
        tasks (list): List of task dictionaries
        priority (str): Priority level to filter by (High, Medium, Low)
        
    Returns:
        list: Filtered list of tasks matching the priority
    """
    return [task for task in tasks if task.get("priority") == priority]

def filter_tasks_by_priority(tasks, priority):
    """Filter tasks by priority level"""
    return [task for task in tasks if task.get("priority") == priority]

def filter_tasks_by_completion(tasks, completed=True):
    """
    Filter tasks by completion status.
    
    Args:
        tasks (list): List of task dictionaries
        completed (bool): Completion status to filter by
        
    Returns:
        list: Filtered list of tasks matching the completion status
    """
    return [task for task in tasks if task.get("completed") == completed]

def search_tasks(tasks, query):
    """
    Search tasks by a text query in title and description.
    
    Args:
        tasks (list): List of task dictionaries
        query (str): Search query
        
    Returns:
        list: Filtered list of tasks matching the search query
    """
    query = query.lower()
    return [
        task for task in tasks 
        if query in task.get("title", "").lower() or 
           query in task.get("description", "").lower()
    ]

def get_overdue_tasks(tasks):
    """Get tasks that are past due date"""
    today = datetime.now().strftime("%Y-%m-%d")
    return [
        task for task in tasks
        if not task.get("completed", False) and 
           task.get("due_date", "") < today
    ]
def get_due_soon_tasks(tasks, hours_threshold=24):
    """
    Get tasks that are due within the specified hours threshold (TDD Feature 1).
    
    Args:
        tasks (list): List of task dictionaries
        hours_threshold (int): Hours window to consider as "due soon"
        
    Returns:
        list: Tasks due within the threshold
    """
    now = datetime.now()
    due_soon = []
    for task in tasks:
        if not task.get("completed", False) and "due_date" in task:
            try:
                due_date = datetime.strptime(task["due_date"], "%Y-%m-%d")
                hours_until_due = (due_date - now).total_seconds() / 3600
                if 0 < hours_until_due <= hours_threshold:
                    due_soon.append(task)
            except ValueError:
                continue
    return due_soon

def add_task_with_category(tasks, title, category, **kwargs):
    """
    Add a new task with custom category (TDD Feature 2).
    
    Args:
        tasks (list): List of existing tasks
        title (str): Task title
        category (str): Task category
        **kwargs: Additional task attributes
        
    Returns:
        list: Updated list of tasks
    """
    new_task = {
        "id": generate_unique_id(tasks),
        "title": title,
        "category": category,
        "completed": False,
        "due_date": (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    new_task.update(kwargs)
    tasks.append(new_task)
    save_tasks(tasks)
    return tasks

def bulk_complete_tasks(tasks, task_ids):
    """
    Mark multiple tasks as completed (TDD Feature 3).
    
    Args:
        tasks (list): List of task dictionaries
        task_ids (list): IDs of tasks to complete
        
    Returns:
        list: Updated list of tasks
    """
    for task in tasks:
        if task["id"] in task_ids:
            task["completed"] = True
    save_tasks(tasks)
    return tasks

def clear_tasks(file_path=DEFAULT_TASKS_FILE):
    """Clear all tasks (for testing)"""
    save_tasks([], file_path)

def count_tasks(file_path=DEFAULT_TASKS_FILE):
    """Count all tasks"""
    return len(load_tasks(file_path))

def get_task_by_title(title, file_path=DEFAULT_TASKS_FILE):
    """Get task by title (for BDD assertions)"""
    tasks = load_tasks(file_path)
    return next((t for t in tasks if t["title"] == title), None)

def filter_tasks_by_category(tasks, category):
    """Filter tasks by category name
    
    Args:
        tasks (list): List of task dictionaries
        category (str): Category name to filter by
        
    Returns:
        list: Filtered list of tasks
    """
    return [task for task in tasks if task.get("category") == category]