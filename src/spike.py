from datetime import datetime
from collections import defaultdict

spike_log = []


def detect_spikes(readings):

    spike_log.clear()
    grouped = defaultdict(list)

    # Group readings by station and date
    for reading in readings:
       if reading["sensor"] == "TEMP":
            grouped[
                (reading["station_id"], reading["timestamp"][:10])
            ].append(reading)

    rejected = set()

    for group in grouped.values():

        group.sort(key=lambda r: datetime.strptime(
            r["timestamp"], "%Y-%m-%d %H:%M:%S"
        ))

        last_accepted = None

        for i, current in enumerate(group):

            value = current["value"]

            # First reading of the day is accepted
            if last_accepted is None:
                last_accepted = current
                continue

            previous_value = last_accepted["value"]

            # Check sudden temperature change
            if abs(value - previous_value) > 5:

                next_reading_is_similar = False

                if i + 1 < len(group):
                    next_value = group[i + 1]["value"]

                    if abs(next_value - value) <= 2:
                        next_reading_is_similar = True

                if not next_reading_is_similar:
                    rejected.add(id(current))
                    spike_log.append(
                        f"Spike rejected: {current}"
                    )
                    continue

            last_accepted = current

    result = [
        reading for reading in readings
        if id(reading) not in rejected
    ]

    return result