import pytest;
from datetime import datetime, timedelta;
from unittest.mock import patch;
from AlmaxUtils.Time import CalculateTimePassed, TimeToString, AddTime;

@pytest.fixture
def fixed_datetime():
    return datetime(2024, 1, 1, 12, 0, 0);

def test_CalculateTimePassed(fixed_datetime):
    start_time = datetime(2024, 1, 1, 10, 0, 0)
    with patch('AlmaxUtils.Time.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        result = CalculateTimePassed(start_time)
        expected = timedelta(hours=2)
        assert result == expected;

def test_TimeToString():
    time = timedelta(days=2, hours=5, minutes=30, seconds=15);
    result = TimeToString(time)
    expected = "2 Days = 53 Hours = 3210 Minutes = 192615.0 Seconds"
    assert result == expected;

def test_AddTime(fixed_datetime):
    hours_to_add = 5
    with patch('AlmaxUtils.Time.datetime') as mock_datetime:
        mock_datetime.now.return_value = fixed_datetime
        mock_datetime.side_effect = lambda *args, **kw: datetime(*args, **kw)
        result = AddTime(hours_to_add)
        expected = (fixed_datetime + timedelta(hours=hours_to_add)).strftime('%d-%m-%Y_%H:%M:%S')
        assert result == expected;