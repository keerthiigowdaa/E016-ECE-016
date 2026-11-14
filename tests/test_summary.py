import sys
sys.path.insert(0, "src")

from summary import generate_daily_summary


def test_daily_summary():

    readings = [
        {"station_id": "ST001", "timestamp": "2026-11-10 09:00",
         "sensor": "temperature", "value": 20},
        {"station_id": "ST001", "timestamp": "2026-11-10 09:15",
         "sensor": "temperature", "value": 30},
        {"station_id": "ST001", "timestamp": "2026-11-10 09:00",
         "sensor": "humidity", "value": 60},
        {"station_id": "ST001", "timestamp": "2026-11-10 09:15",
         "sensor": "humidity", "value": 80},
        {"station_id": "ST001", "timestamp": "2026-11-10 09:00",
         "sensor": "rainfall", "value": 5}
    ]

    result = generate_daily_summary(
        "ST001", "2026-11-10", readings
    )

    assert result["temperature_min"] == 20
    assert result["temperature_max"] == 30
    assert result["temperature_mean"] == 25
    assert result["humidity_mean"] == 70
    assert result["rainfall_total"] == 5

    print("Daily summary test passed!")


if __name__ == "__main__":
    test_daily_summary()