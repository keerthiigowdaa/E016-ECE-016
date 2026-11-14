from datetime import datetime, timedelta
from collections import defaultdict

filled_readings = []


def interpolate_missing(readings):

    filled_readings.clear()
    grouped = defaultdict(dict)

    # Group readings by station, date and sensor
    for reading in readings:
        if reading["sensor"] == "RAIN":

            continue

        timestamp = datetime.strptime(
            reading["timestamp"],"%Y-%m-%d %H:%M:%S" 
        )

        key = (
            reading["station_id"],
            timestamp.date(),
            reading["sensor"]
        )

        grouped[key][timestamp] = reading["value"]

    # Find gaps and fill up to 4 consecutive missing readings
    for key, values in grouped.items():

        timestamps = sorted(values)

        for i in range(len(timestamps) - 1):

            start = timestamps[i]
            end = timestamps[i + 1]

            gap = int((end - start).total_seconds() // 900) - 1

            if 1 <= gap <= 4:

                start_value = values[start]
                end_value = values[end]

                difference = (end_value - start_value) / (gap + 1)

                for step in range(1, gap + 1):

                    missing_time = start + timedelta(minutes=15 * step)
                    missing_value = start_value + difference * step

                    filled_readings.append({
                        "station_id": key[0],
                        "timestamp": missing_time.strftime(
                            "%Y-%m-%d %H:%M"
                        ),
                        "sensor": key[2],
                        "value": round(missing_value, 2),
                        "filled": True
                    })

    print("Interpolation completed!")
    print("Filled readings:", len(filled_readings))

    return readings + filled_readings