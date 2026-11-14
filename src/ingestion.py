from datetime import datetime

readings = []


def add_reading(station_id, timestamp, sensor, value):

    try:
        datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("Invalid timestamp!")
        return

    reading = {
        "station_id": station_id,
        "timestamp": timestamp,
        "sensor": sensor.upper(),
        "value": float(value)
    }

    readings.append(reading)
    print("Reading added successfully!")


def display_readings():

    for reading in readings:
        print(reading)