from behave import *
from datetime import datetime, timedelta
from src.tasks import (
    load_tasks, 
    save_tasks, 
    add_task_with_category,
    filter_tasks_by_priority,
    get_overdue_tasks,
    bulk_complete_tasks
)

def parse_due_date(due_date_str):
    due_date_str = due_date_str.lower()
    if due_date_str == "today":
        return datetime.now().strftime("%Y-%m-%d")
    elif due_date_str == "tomorrow":
        return (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    elif due_date_str == "yesterday":
        return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    return due_date_str

@given('I start with an empty task list')
def step_impl(context):
    context.tasks = []
    save_tasks(context.tasks)

@given('I have a task "{title}" in my list')
def step_impl(context, title):
    context.tasks = load_tasks()
    if not any(t['title'] == title for t in context.tasks):
        add_task_with_category(
            context.tasks,
            title,
            "General",
            due_date=(datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        )
        save_tasks(context.tasks)

@given('I have these tasks')
def step_impl(context):
    for row in context.table:
        add_task_with_category(
            context.tasks,
            row['Title'],
            "General",
            priority=row.get('Priority', 'Medium'),
            due_date=parse_due_date(row.get('Due Date', 'Tomorrow'))
        )
    save_tasks(context.tasks)

@given('I have a task "{title}" due yesterday')
def step_impl(context, title):
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    add_task_with_category(
        context.tasks,
        title,
        "General",
        due_date=yesterday
    )
    save_tasks(context.tasks)

@when('I add a task "{title}" with')
def step_impl(context, title):
    task_data = {row['Field']: row['Value'] for row in context.table}
    add_task_with_category(
        context.tasks,
        title,
        task_data.get('Category', 'General'),
        priority=task_data.get('Priority', 'Medium'),
        due_date=parse_due_date(task_data.get('Due Date', 'Tomorrow'))
    )
    save_tasks(context.tasks)

@when('I mark "{title}" as completed')
def step_impl(context, title):
    tasks = load_tasks()
    task_ids = [t['id'] for t in tasks if t['title'] == title]
    bulk_complete_tasks(tasks, task_ids)

@when('I filter by "{priority}" priority')
def step_impl(context, priority):
    context.filtered_tasks = filter_tasks_by_priority(load_tasks(), priority)

@when('I delete "{title}"')
def step_impl(context, title):
    tasks = [t for t in load_tasks() if t['title'] != title]
    save_tasks(tasks)

@when('I view overdue tasks')
def step_impl(context):
    context.overdue_tasks = get_overdue_tasks(load_tasks())

@then('I should see "{title}" in my tasks')
def step_impl(context, title):
    tasks = load_tasks()
    assert any(t['title'] == title for t in tasks), f"Task '{title}' not found"

@then('it should have priority "{priority}"')
def step_impl(context, priority):
    tasks = load_tasks()
    assert tasks[-1]['priority'] == priority, f"Expected {priority}, got {tasks[-1]['priority']}"

@then('it should belong to category "{category}"')
def step_impl(context, category):
    tasks = load_tasks()
    assert tasks[-1]['category'] == category, f"Expected {category}, got {tasks[-1]['category']}"

@then('the task should show as completed')
def step_impl(context):
    tasks = load_tasks()
    assert tasks[-1]['completed'] is True, "Task was not completed"

@then('I should only see "{title}"')
def step_impl(context, title):
    assert len(context.filtered_tasks) == 1, f"Expected 1 task, got {len(context.filtered_tasks)}"
    assert context.filtered_tasks[0]['title'] == title

@then('it should not appear in my tasks')
def step_impl(context):
    tasks = load_tasks()
    assert len(tasks) == 0, f"Tasks still exist: {tasks}"

@then('I should see "{title}" in the overdue list')
def step_impl(context, title):
    assert any(t['title'] == title for t in context.overdue_tasks), \
        f"'{title}' not in overdue tasks: {context.overdue_tasks}"