import csv

stations = {}

sensor_ranges = {}


def register_station(station_id, district, available_sensors=None):

    if station_id in stations:
        print("Station already exists!")
        return

    if available_sensors is None:
        available_sensors = {
            "temperature": (-10, 50),
            "humidity": (0, 100),
            "rainfall": (0, 100)
        }

    stations[station_id] = {
        "district": district,
        "sensors": available_sensors
    }


def load_sensor_ranges(filename):

    sensor_ranges.clear()

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            sensor_ranges[row["sensor"]] = (
                float(row["min_value"]),
                float(row["max_value"])
            )

    print("Sensor ranges loaded:", len(sensor_ranges))


def load_stations(filename):

    stations.clear()

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            available_sensors = {}

            sensor_names = row["sensors"].split(";")

            for sensor in sensor_names:
                if sensor in sensor_ranges:
                    available_sensors[sensor] = sensor_ranges[sensor]

            stations[row["station_id"]] = {
                "name": row["station_name"],
                "district": row["district"],
                "sensors": available_sensors
            }

    print("Stations loaded:", len(stations))


def display_stations():

    if not stations:
        print("No stations registered.")
        return

    for station_id, details in stations.items():
        print("Station ID:", station_id)
        print("District:", details["district"])
        print("Sensors:", details["sensors"])
        print("--------------------------")