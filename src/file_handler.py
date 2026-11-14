import csv
from ingestion import add_reading


def load_readings(filename):

    try:
        with open(filename, "r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:
                add_reading(
                    row["station_id"],
                    row["timestamp"],
                    row["sensor"],
                    row["value"]
                )

        print("CSV data loaded successfully!")

    except FileNotFoundError:
        print("Input file not found!")

    except KeyError:
        print("CSV columns are incorrect!")