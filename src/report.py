
import csv
import os


def save_qa_log(qa_log):

    os.makedirs("output", exist_ok=True)

    with open("output/qa_log.txt", "w") as file:
        for message in qa_log:
            file.write(str(message) + "\n")

    print("QA log saved successfully!")


def save_daily_summaries(summaries):

    os.makedirs("output", exist_ok=True)

    fields = [
        "date", "station_id", "district", "status",
        "temp_min", "temp_max", "temp_mean",
        "humidity_min", "humidity_max", "humidity_mean",
        "rainfall_mm", "missing_temp",
        "missing_humidity", "missing_rain", "alert_level"
    ]

    with open("output/daily_summary.csv", "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for summary in sorted(
            summaries,
            key=lambda x: (x["date"], x["station_id"])
        ):
            writer.writerow(summary)

    print("Daily summaries saved successfully!")


def save_district_alerts(alerts):

    os.makedirs("output", exist_ok=True)

    fields = [
        "date", "district", "alert_level",
        "max_station_id", "max_rainfall_mm"
    ]

    with open("output/district_alerts.csv", "w", newline="") as file:

        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()

        for key, alert in sorted(alerts.items()):
            writer.writerow({
                "date": key[0],
                "district": key[1],
                **alert
            })

    print("District alerts saved successfully!")
