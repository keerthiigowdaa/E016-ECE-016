

def generate_district_alerts(summaries):

    district_alerts = {}

    priority = {
        "NONE": 0,
        "HEAVY": 1,
        "VERY_HEAVY": 2,
        "EXTREMELY_HEAVY": 3
    }

    for summary in summaries:

        if summary.get("status") == "INVALID":
            continue

        rainfall = summary["rainfall_mm"]
        district = summary["district"]
        station_id = summary["station_id"]
        date = summary["date"]

        if rainfall > 204.4:
            alert = "EXTREMELY_HEAVY"
        elif rainfall > 115.5:
            alert = "VERY_HEAVY"
        elif rainfall > 64.5:
            alert = "HEAVY"
        else:
            alert = "NONE"

        key = (date, district)

        if key not in district_alerts:
            district_alerts[key] = {
                "alert_level": alert,
                "max_station_id": station_id,
                "max_rainfall_mm": rainfall
            }

        else:
            current = district_alerts[key]

            if rainfall > current["max_rainfall_mm"] or (
                rainfall == current["max_rainfall_mm"]
                and station_id < current["max_station_id"]
            ):
                current["max_station_id"] = station_id
                current["max_rainfall_mm"] = rainfall

            if priority[alert] > priority[current["alert_level"]]:
                current["alert_level"] = alert

    return district_alerts
