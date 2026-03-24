import pytest
from unittest.mock import patch
from unittest.mock import MagicMock
from db_repository import read_oura_daily_data

# this function does
# cursor() → execute(SQL) → fetchone() → convert tuple → dict

def test_gethealthstatdb():
    mock_conn = MagicMock() #fake connection
    mock_cursor = MagicMock() #fake cursor
    mock_conn.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (
                            "2026-03-14",
                            85,
                            25200,
                            55,
                            60,
                            82
                            )

    results = read_oura_daily_data(mock_conn)

    fake_resultdict = {
            "day": "2026-03-14",
            "sleep_score": 85,
            "total_sleep_duration": 25200,
            "average_hrv": 55,
            "resting_heart_rate": 60,
            "readiness_score": 82
        }

    assert isinstance (results, dict)
    assert results == fake_resultdict

