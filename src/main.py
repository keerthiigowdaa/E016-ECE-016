from station import load_sensor_ranges, load_stations, stations
from file_handler import load_readings
from validation import validate_readings, accepted_readings, qa_log
from spike import detect_spikes, spike_log
from report import save_qa_log, save_daily_summaries, save_district_alerts
from interpolation import interpolate_missing
from completeness import check_completeness
from summary import generate_daily_summary
from alerts import generate_district_alerts

print("====================================")
print(" WEATHER STATION DATA QA SYSTEM")
print("====================================")

# STEP 1: Register stations
print("\nREGISTERING STATIONS")

load_sensor_ranges("input/sensor_ranges.csv")
load_stations("input/stations.csv")

# STEP 2: Load CSV readings
print("\nLOADING WEATHER DATA")

load_readings("input/readings.csv")

# STEP 3: Validate readings
print("\nVALIDATING DATA")

validate_readings()

# STEP 4: Detect temperature spikes
print("\nDETECTING SPIKES")

accepted_readings[:] = detect_spikes(accepted_readings)
qa_log.extend(spike_log)

# STEP 5: Interpolate missing data
print("\nINTERPOLATING MISSING DATA")

processed_readings = interpolate_missing(accepted_readings)


# STEP 6: Check daily completeness
station_days = set()

for reading in processed_readings:
    station_days.add((
        reading["station_id"],
        reading["timestamp"][:10]
    ))

print("\nCHECKING DAILY COMPLETENESS")

station_day_status = {}

for station_id, date in sorted(station_days):

    result = check_completeness(
        station_id,
        date,
        processed_readings
    )

    station_day_status[(station_id, date)] = result

# STEP 7: Generate daily summaries
print("\nGENERATING DAILY SUMMARIES")

station_summaries = []

for station_id, date in sorted(station_days):

    summary = generate_daily_summary(
        station_id,
        date,
        processed_readings
    )

    if summary is not None:

        completeness = station_day_status[(station_id, date)]

        if completeness["status"] == "INVALID":
            continue

        summary["district"] = stations[station_id]["district"]
        summary["status"] = completeness["status"]

        summary["missing_temp"] = completeness["missing_temp"]
        summary["missing_humidity"] = completeness["missing_humidity"]
        summary["missing_rain"] = completeness["missing_rain"]

        rainfall = summary["rainfall_mm"]

        if rainfall > 204.4:
            summary["alert_level"] = "EXTREMELY_HEAVY"
        elif rainfall > 115.5:
            summary["alert_level"] = "VERY_HEAVY"
        elif rainfall > 64.5:
            summary["alert_level"] = "HEAVY"
        else:
            summary["alert_level"] = "NONE"

        station_summaries.append(summary)

        print("\nDaily Summary:")
        print(summary)

# STEP 8: Generate district rainfall alerts
print("\nGENERATING DISTRICT RAINFALL ALERTS")

district_alerts = generate_district_alerts(station_summaries)

for district, alert in district_alerts.items():
    print(district, ":", alert)

save_daily_summaries(station_summaries)
save_district_alerts(district_alerts)

# STEP 9: Save QA report
print("\nSAVING QA REPORT")

save_qa_log(qa_log)

# FINAL OUTPUT
print("\n====================================")
print(" PROJECT EXECUTION COMPLETED!")
print("====================================")

print("Accepted readings:", len(accepted_readings))
print("Rejected readings:", len(qa_log))
print("Interpolated readings:", len(processed_readings) - len(accepted_readings))
print("Daily summaries generated:", len(station_summaries))
print("District alerts generated:", len(district_alerts))