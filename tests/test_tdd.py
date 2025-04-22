import pytest
from src.tasks import load_tasks, save_tasks
from datetime import datetime, timedelta

# Feature 1: Task due date notifications
def test_task_due_soon_notification():
    """Test notification for tasks due soon"""
    tasks = [{
        "id": 1,
        "title": "Urgent task",
        "due_date": (datetime.now() + timedelta(hours=23)).strftime("%Y-%m-%d"),  # Due in 23 hours
        "completed": False
    }]
    
    from src.tasks import get_due_soon_tasks
    due_soon = get_due_soon_tasks(tasks)
    assert len(due_soon) == 1
    assert "Urgent task" in due_soon[0]["title"]

# Feature 2: Task categories management
def test_add_new_category():
    """Test adding tasks with new categories"""
    tasks = []
    from src.tasks import add_task_with_category
    tasks = add_task_with_category(tasks, "New task", "CustomCategory")
    assert tasks[0]["category"] == "CustomCategory"

# Feature 3: Bulk task operations
def test_bulk_complete_tasks():
    """Test completing multiple tasks at once"""
    tasks = [
        {"id": 1, "title": "Task 1", "completed": False},
        {"id": 2, "title": "Task 2", "completed": False}
    ]
    from src.tasks import bulk_complete_tasks
    updated_tasks = bulk_complete_tasks(tasks, [1, 2])
    assert updated_tasks[0]["completed"] is True
    assert updated_tasks[1]["completed"] is True