
def generate_daily_summary(station_id, date, readings):

    temperatures = []
    humidity_values = []
    rainfall_values = []

    for reading in readings:
        if reading["station_id"] != station_id:
            continue

        if reading["timestamp"][:10] != date:
            continue

        sensor = reading["sensor"].upper()
        value = reading["value"]

        if sensor == "TEMP":
            temperatures.append(value)
        elif sensor == "HUMIDITY":
            humidity_values.append(value)
        elif sensor == "RAIN":
            rainfall_values.append(value)

    return {
        "date": date,
        "station_id": station_id,
        "temp_min": round(min(temperatures), 1) if temperatures else None,
        "temp_max": round(max(temperatures), 1) if temperatures else None,
        "temp_mean": round(sum(temperatures) / len(temperatures), 1) if temperatures else None,
        "humidity_min": round(min(humidity_values), 1) if humidity_values else None,
        "humidity_max": round(max(humidity_values), 1) if humidity_values else None,
        "humidity_mean": round(sum(humidity_values) / len(humidity_values), 1) if humidity_values else None,
        "rainfall_mm": round(sum(rainfall_values), 1),
    }