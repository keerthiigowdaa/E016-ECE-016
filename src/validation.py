from station import stations
from ingestion import readings

accepted_readings = []
qa_log = []


def validate_readings():

    accepted_readings.clear()
    qa_log.clear()

    seen = set()

    for reading in readings:

        station_id = reading["station_id"]
        timestamp = reading["timestamp"]
        sensor = reading["sensor"]
        value = reading["value"]

        # Check station registration
        if station_id not in stations:
            qa_log.append(f"Rejected: Unknown station {station_id}")
            continue

        # Check sensor name
        if sensor not in stations[station_id]["sensors"]:
            qa_log.append(f"Rejected: Invalid sensor {sensor}")
            continue

        # Check duplicate readings
        key = (station_id, timestamp, sensor)

        if key in seen:
            qa_log.append(f"Rejected duplicate: {key}")
            continue

        seen.add(key)

        # Check valid sensor range
        minimum, maximum = stations[station_id]["sensors"][sensor]

        if not minimum <= value <= maximum:
            qa_log.append(f"Rejected out-of-range reading: {key}")
            continue

        accepted_readings.append(reading)

    print("\nVALIDATION COMPLETED")
    print("Accepted readings:", len(accepted_readings))
    print("Rejected readings:", len(qa_log))

    for message in qa_log:
        print(message)