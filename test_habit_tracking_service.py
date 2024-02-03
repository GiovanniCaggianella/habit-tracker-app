import pytest
from unittest.mock import patch
from habit_tracking_service import calculate_streak, get_habit_longest_streak_by_habit_id, get_habits_ordered_by_longest_streak, get_most_long_streak_habit, get_worst_ever_streak_habit, get_last_month_worst_habit
from models import Habit, HabitTracking

@pytest.fixture
def mock_session():
    # Mock the database session
    with patch('habit_tracking_service.Session') as mock:
        yield mock

@pytest.fixture
def sample_habits():
    return [
        Habit(id=1, title="Read", description="Read a book", created_at=1704067200, fk_user=1, fk_habit_type=1),
        Habit(id=2, title="Exercise", description="Go for a run", created_at=1704067200, fk_user=1, fk_habit_type=2),
        Habit(id=3, title="Meditate", description="Practice meditation", created_at=1704067200, fk_user=1, fk_habit_type=3),
    ]

@pytest.fixture
def sample_habit_trackings_habit_one():
    return [
        HabitTracking(id=1, fk_habit=1, checked_at=1704067200.0),  # Jan 1, 2024
        HabitTracking(id=2, fk_habit=1, checked_at=1704153600.0),  # Jan 2, 2024
        HabitTracking(id=3, fk_habit=1, checked_at=1704240000.0),  # Jan 3, 2024
        HabitTracking(id=4, fk_habit=1, checked_at=1704326400.0),  # Jan 4, 2024
        HabitTracking(id=5, fk_habit=1, checked_at=1704412800.0),  # Jan 5, 2024
        HabitTracking(id=6, fk_habit=1, checked_at=1704499200.0),  # Jan 6, 2024
        HabitTracking(id=7, fk_habit=1, checked_at=1704585600.0),  # Jan 7, 2024
        HabitTracking(id=8, fk_habit=1, checked_at=1704672000.0),  # Jan 8, 2024
        #HabitTracking(id=9, fk_habit=1, checked_at=1704758400.0),  # Jan 9, 2024
        #HabitTracking(id=10, fk_habit=1, checked_at=1704844800.0), # Jan 10, 2024
        HabitTracking(id=11, fk_habit=1, checked_at=1704931200.0), # Jan 11, 2024
        HabitTracking(id=12, fk_habit=1, checked_at=1705017600.0), # Jan 12, 2024
        HabitTracking(id=13, fk_habit=1, checked_at=1705104000.0), # Jan 13, 2024
        HabitTracking(id=14, fk_habit=1, checked_at=1705190400.0), # Jan 14, 2024
        HabitTracking(id=15, fk_habit=1, checked_at=1705276800.0), # Jan 15, 2024
        HabitTracking(id=16, fk_habit=1, checked_at=1705363200.0), # Jan 16, 2024
        HabitTracking(id=17, fk_habit=1, checked_at=1705449600.0), # Jan 17, 2024
        HabitTracking(id=18, fk_habit=1, checked_at=1705536000.0), # Jan 18, 2024
        HabitTracking(id=19, fk_habit=1, checked_at=1705622400.0), # Jan 19, 2024
        HabitTracking(id=20, fk_habit=1, checked_at=1705708800.0), # Jan 20, 2024
    ]

@pytest.fixture
def sample_habit_trackings():
    return [
        HabitTracking(id=1, fk_habit=1, checked_at=1705104000.0),
        HabitTracking(id=2, fk_habit=1, checked_at=1705276800.0),
        HabitTracking(id=3, fk_habit=1, checked_at=1706572800.0),
        HabitTracking(id=4, fk_habit=1, checked_at=1706227200.0),
        HabitTracking(id=5, fk_habit=1, checked_at=1704499200.0),
        HabitTracking(id=6, fk_habit=1, checked_at=1705622400.0),
        HabitTracking(id=7, fk_habit=1, checked_at=1705190400.0),
        HabitTracking(id=8, fk_habit=1, checked_at=1704758400.0),
        HabitTracking(id=9, fk_habit=1, checked_at=1704585600.0),
        HabitTracking(id=10, fk_habit=1, checked_at=1704672000.0),
        HabitTracking(id=11, fk_habit=1, checked_at=1706659200.0),
        HabitTracking(id=12, fk_habit=1, checked_at=1705881600.0),
        HabitTracking(id=13, fk_habit=1, checked_at=1705708800.0),
        HabitTracking(id=14, fk_habit=1, checked_at=1705449600.0),
        HabitTracking(id=15, fk_habit=3, checked_at=1705536000.0),
        HabitTracking(id=16, fk_habit=1, checked_at=1704240000.0),
        HabitTracking(id=17, fk_habit=2, checked_at=1705795200.0),
        HabitTracking(id=18, fk_habit=3, checked_at=1704412800.0),
        HabitTracking(id=19, fk_habit=2, checked_at=1704326400.0),
        HabitTracking(id=20, fk_habit=2, checked_at=1706486400.0),
        HabitTracking(id=21, fk_habit=3, checked_at=1705017600.0),
        HabitTracking(id=22, fk_habit=1, checked_at=1704844800.0),
        HabitTracking(id=23, fk_habit=1, checked_at=1706140800.0),
        HabitTracking(id=24, fk_habit=3, checked_at=1705363200.0),
        HabitTracking(id=25, fk_habit=1, checked_at=1706313600.0),
        HabitTracking(id=26, fk_habit=2, checked_at=1704067200.0),
        HabitTracking(id=27, fk_habit=1, checked_at=1704931200.0),
        HabitTracking(id=28, fk_habit=1, checked_at=1704153600.0),
        HabitTracking(id=29, fk_habit=1, checked_at=1705968000.0),
        HabitTracking(id=30, fk_habit=1, checked_at=1706054400.0),
    ]

def test_get_most_long_streak_habit(mock_session, sample_habits, sample_habit_trackings):

    mock_session.return_value.query.return_value.all.return_value = sample_habits
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = sample_habit_trackings

    result = get_most_long_streak_habit()

    assert result == sample_habits[0]

def test_get_worst_ever_streak_habit(mock_session, sample_habits, sample_habit_trackings):

    mock_session.return_value.query.return_value.all.return_value = sample_habits
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = sample_habit_trackings

    result = get_worst_ever_streak_habit()

    assert result == sample_habits[0]

def test_get_last_month_worst_habit(mock_session, sample_habits, sample_habit_trackings):

    mock_session.return_value.query.return_value.all.return_value = sample_habits
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = sample_habit_trackings

    result = get_last_month_worst_habit()

    assert result == sample_habits[0]

def test_calculate_streak(sample_habit_trackings_habit_one):

    longest_streak, longest_start, longest_end = calculate_streak(sample_habit_trackings_habit_one)

    assert longest_streak == 10
    assert longest_start == 1704931200.0
    assert longest_end == 1705708800.0

def test_get_habits_ordered_by_longest_streak(mock_session, sample_habits, sample_habit_trackings):
    
    mock_session.return_value.query.return_value.filter.return_value.all.return_value = sample_habits
    mock_session.return_value.query.return_value.filter.return_value.order_by.return_value.all.return_value = sample_habit_trackings

    result = get_habits_ordered_by_longest_streak(1)

    assert len(result.field_names) == 5
    assert result.field_names[0] == "Habit ID"
    assert result.field_names[1] == "Title"
    assert result.field_names[2] == "Longest Streak"
    assert result.field_names[3] == "Streak Start Date"
    assert result.field_names[4] == "Streak End Date"
    assert len(result._rows) == 3
    assert result._rows[0][0] == 1
    assert result._rows[0][1] == "Read"
    assert result._rows[0][2] == 2
    assert result._rows[0][3] == "2024-01-07"
    assert result._rows[0][4] == "2024-01-08"
    assert result._rows[1][0] == 2
    assert result._rows[1][1] == "Exercise"
    assert result._rows[1][2] == 2
    assert result._rows[1][3] == "2024-01-07"
    assert result._rows[1][4] == "2024-01-08"
    assert result._rows[2][0] == 3
    assert result._rows[2][1] == "Meditate"
    assert result._rows[2][2] == 2
    assert result._rows[2][3] == "2024-01-07"
    assert result._rows[2][4] == "2024-01-08"

def test_get_habit_longest_streak_by_habit_id(mock_session, sample_habits, sample_habit_trackings_habit_one):
    
    habit_id = 1
    mock_session.return_value.query.return_value.filter.return_value.first.return_value = sample_habits[0]
    mock_session.return_value.query.return_value.filter.return_value.order_by.return_value.all.return_value = sample_habit_trackings_habit_one

    result = get_habit_longest_streak_by_habit_id(habit_id)

    assert len(result.field_names) == 5
    assert result.field_names[0] == "Habit ID"
    assert result.field_names[1] == "Title"
    assert result.field_names[2] == "Longest Streak"
    assert result.field_names[3] == "Streak Start Date"
    assert result.field_names[4] == "Streak End Date"
    assert len(result._rows) == 1
    assert result._rows[0][0] == 1
    assert result._rows[0][1] == "Read"
    assert result._rows[0][2] == 10
    assert result._rows[0][3] == "2024-01-11"
    assert result._rows[0][4] == "2024-01-20"
