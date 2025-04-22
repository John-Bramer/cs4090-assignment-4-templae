import pytest
from src.tasks import load_tasks, save_tasks, filter_tasks_by_priority
from unittest.mock import patch, mock_open

@pytest.fixture
def sample_tasks():
    return [
        {"id": 1, "title": "Task 1", "priority": "High", "completed": False},
        {"id": 2, "title": "Task 2", "priority": "Low", "completed": True}
    ]

# Parameterized test
@pytest.mark.parametrize("priority,expected", [
    ("High", 1),
    ("Low", 1),
    ("Medium", 0)
])
def test_parametrized(sample_tasks, priority, expected):
    result = filter_tasks_by_priority(sample_tasks, priority)
    assert len(result) == expected

# Mocking test
def test_mock():
    with patch("builtins.open", mock_open(read_data='[]')):
        tasks = load_tasks("fake.json")
        assert tasks == []
    
    with patch("json.dump") as mock_dump:
        save_tasks([], "fake.json")
        assert mock_dump.called