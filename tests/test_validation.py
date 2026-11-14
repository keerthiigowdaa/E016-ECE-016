import sys
sys.path.insert(0, "src")

from station import register_station
from ingestion import readings, add_reading
from validation import validate_readings, accepted_readings, qa_log

def test_validation():

    readings.clear()
    accepted_readings.clear()
    qa_log.clear()

    register_station("TEST01", "Bengaluru")

    add_reading("TEST01", "2026-11-10 09:00", "temperature", 28)
    add_reading("TEST01", "2026-11-10 09:15", "temperature", 55)
    add_reading("TEST01", "2026-11-10 09:00", "temperature", 28)

    validate_readings()

    assert len(accepted_readings) == 1
    assert len(qa_log) == 2

    print("All validation tests passed!")


if __name__ == "__main__":
    test_validation()