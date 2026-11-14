
from datetime import datetime


def check_completeness(station_id, date, readings):

    sensors = ["TEMP", "HUMIDITY", "RAIN"]

    received = {
        sensor: set()
        for sensor in sensors
    }

    for reading in readings:

        if reading["station_id"] != station_id:
            continue

        timestamp_text = reading["timestamp"]

        if len(timestamp_text) == 19:
            timestamp = datetime.strptime(
                timestamp_text, "%Y-%m-%d %H:%M:%S"
            )
        else:
            timestamp = datetime.strptime(
                timestamp_text, "%Y-%m-%d %H:%M"
            )

        if timestamp.strftime("%Y-%m-%d") != date:
            continue

        sensor = reading["sensor"].upper()

        if sensor in received:
            received[sensor].add(timestamp)

    missing = {
        sensor: max(0, 96 - len(received[sensor]))
        for sensor in sensors
    }

    total_missing = sum(missing.values())
    expected = 96 * len(sensors)

    status = (
        "INVALID"
        if (total_missing / expected) * 100 > 20
        else "VALID"
    )

    print("Station-day status:", status)

    return {
        "status": status,
        "missing_temp": missing["TEMP"],
        "missing_humidity": missing["HUMIDITY"],
        "missing_rain": missing["RAIN"]
    }
