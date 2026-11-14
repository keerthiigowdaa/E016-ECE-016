from src.completeness import check_completeness
from datetime import datetime, timedelta


def test_complete_day():
    readings = []
    start = datetime(2026, 1, 1, 0, 0)

    for i in range(96):
        timestamp = (start + timedelta(minutes=15 * i)).strftime(
            "%Y-%m-%d %H:%M"
        )

        for sensor in ["temperature", "humidity", "rainfall"]:
            readings.append({
                "station_id": "S1",
                "timestamp": timestamp,
                "sensor": sensor
            })

    result = check_completeness("S1", "2026-01-01", readings)

    assert result is True


def test_incomplete_day():
    readings = []

    for i in range(10):
        timestamp = f"2026-01-01 00:{i:02d}"

        readings.append({
            "station_id": "S1",
            "timestamp": timestamp,
            "sensor": "temperature"
        })

    result = check_completeness("S1", "2026-01-01", readings)

    assert result is False