from datetime import datetime
import pytest
from habit_tracking_service import add_new_habit, get_all_habit_by_user_id_and_habit_type_id, remove_habit, update_habit
from unittest.mock import ANY, MagicMock, patch

from models import Habit

@pytest.fixture
def session_mock():
    session = MagicMock()
    session.query.return_value.join.return_value.filter.return_value.all.return_value = [
        (MagicMock(id=1, title="Test Habit"), "Habit Type Description")
    ]
    return session

@pytest.fixture
def mock_session(session_mock):
    with patch('habit_tracking_service.Session', return_value=session_mock) as mock:
        yield mock

def test_get_all_habit_by_user_id_and_habit_type_id():
    habits = get_all_habit_by_user_id_and_habit_type_id(1, None)
    assert len(habits) == 1
    assert habits[0][0] == 1
    assert habits[0][1] == "Test Habit"

def test_add_new_habit():
    title = "Test Habit"
    description = "Test Description"
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fk_user = 1
    fk_habit_type = 1

    new_habit = add_new_habit(title, description, created_at, fk_user, fk_habit_type)

    assert new_habit.title == title
    assert new_habit.description == description
    assert new_habit.created_at == created_at
    assert new_habit.fk_user == fk_user
    assert new_habit.fk_habit_type == fk_habit_type

def test_update_habit():
    habit_id = 1
    title = "Updated Habit"
    description = "Updated Description"
    fk_habit_type = 2

    updated_habit = update_habit(habit_id, title, description, fk_habit_type)

    assert updated_habit.title == title
    assert updated_habit.description == description
    assert updated_habit.fk_habit_type == fk_habit_type

def test_remove_habit():
    habit_id = 1
    session_mock = MagicMock()

    habit_mock = MagicMock()
    session_mock.query.return_value.filter.return_value.first.return_value = habit_mock

    with patch('habit_tracking_service.Session', return_value=session_mock):
        remove_habit(habit_id)

    session_mock.query.assert_called_once_with(Habit)
    session_mock.query.return_value.filter.assert_called_once_with(ANY)
    session_mock.query.return_value.filter.return_value.first.assert_called_once()
    session_mock.delete.assert_called_once_with(ANY)
    session_mock.commit.assert_called_once()