import pytest
import os
import json
from datetime import datetime, timedelta
from src.tasks import (
    load_tasks, save_tasks, generate_unique_id,
    filter_tasks_by_priority, filter_tasks_by_category,
    filter_tasks_by_completion, search_tasks, get_overdue_tasks
)

TEST_FILE = "test_tasks.json"

@pytest.fixture
def sample_tasks():
    return [
        {
            "id": 1,
            "title": "Test Task 1",
            "description": "Something important",
            "priority": "High",
            "category": "Work",
            "due_date": "2000-01-01",  # Past date
            "completed": False
        },
        {
            "id": 2,
            "title": "Buy milk",
            "description": "Grocery shopping",
            "priority": "Low",
            "category": "Personal",
            "due_date": "2099-01-01",
            "completed": True
        }
    ]

def test_generate_unique_id(sample_tasks):
    assert generate_unique_id(sample_tasks) == 3

def test_filter_by_priority(sample_tasks):
    result = filter_tasks_by_priority(sample_tasks, "High")
    assert len(result) == 1
    assert result[0]["priority"] == "High"

def test_filter_by_category(sample_tasks):
    result = filter_tasks_by_category(sample_tasks, "Work")
    assert len(result) == 1
    assert result[0]["category"] == "Work"

def test_filter_by_completion(sample_tasks):
    result = filter_tasks_by_completion(sample_tasks, completed=False)
    assert len(result) == 1
    assert result[0]["completed"] is False

def test_search_tasks(sample_tasks):
    result = search_tasks(sample_tasks, "milk")
    assert len(result) == 1
    assert "milk" in result[0]["title"].lower()

def test_get_overdue_tasks(sample_tasks):
    result = get_overdue_tasks(sample_tasks)
    assert len(result) == 1
    assert result[0]["due_date"] < datetime.now().strftime("%Y-%m-%d")

def test_save_and_load_tasks(sample_tasks):
    save_tasks(sample_tasks, file_path=TEST_FILE)
    loaded = load_tasks(file_path=TEST_FILE)
    assert loaded == sample_tasks
    os.remove(TEST_FILE)

def test_load_tasks_file_not_found(tmp_path):
    fake_file = tmp_path / "nonexistent.json"
    tasks = load_tasks(str(fake_file))
    assert tasks == []

def test_load_tasks_invalid_json(tmp_path, capsys):
    bad_file = tmp_path / "bad.json"
    bad_file.write_text("{ not: valid json }")
    tasks = load_tasks(str(bad_file))
    captured = capsys.readouterr()
    assert "invalid JSON" in captured.out
    assert tasks == []

def test_generate_unique_id_with_existing_tasks():
    tasks = [{"id": 1}, {"id": 2}, {"id": 5}]
    new_id = generate_unique_id(tasks)
    assert new_id == 6