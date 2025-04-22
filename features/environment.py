from behave import fixture
from src.tasks import clear_tasks, save_tasks
import os

@fixture
def clean_tasks_before_scenario(context):
    # Runs before each scenario
    clear_tasks()
    yield
    # Runs after each scenario
    if os.path.exists("test_tasks.json"):
        os.remove("test_tasks.json")

def before_scenario(context, scenario):
    clean_tasks_before_scenario(context)
    context.tasks_file = "test_tasks.json"  # Use test file