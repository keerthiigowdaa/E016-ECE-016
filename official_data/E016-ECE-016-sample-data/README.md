# ECE-016 – Weather-Station Data QA and Daily Summary Engine — Sample Data Pack
Prepared by 10 SECONDS for Team E016.

This pack is the input for a weather-station QA engine: 8 automatic weather stations in 3 districts of coastal and hill Karnataka, 15-minute TEMP / HUMIDITY / RAIN readings from 2026-10-05 to 2026-10-07. Your engine reads `commands.txt`, validates every reading, fills short gaps, and prints the QA log, a daily summary per station and the district rainfall alerts.

Pack conventions where the brief is silent: a day has 96 slots, 00:00:00 to 23:45:00, and every reading is one slot. A slot is missing for a sensor when no row was sent or its reading was rejected (range, spike or duplicate). Checks run in this order: range → duplicate → spike → interpolation. The spike check uses the previous ACCEPTED TEMP reading of the same station on the same day (the first TEMP reading of each day has no previous value) and the next TEMP reading of that station that passes the range check. Interpolation needs an accepted neighbour on both sides on the same day; FILLED values are rounded to 1 decimal and those rounded values are used in the summary. Day validity is checked per sensor after filling: if any sensor of a station-day has more than 20% of its 96 slots missing (20 or more), the station-day is INVALID. INVALID station-days get no summary values and do not feed district alerts. Rainfall totals are rounded to 1 decimal before comparing with the alert thresholds.

## Files
| File | What it holds | Rows |
|---|---|---|
| stations.csv | Weather stations with district | 8 |
| sensor_ranges.csv | Valid range per sensor (from the brief) | 3 |
| readings.csv | 15-minute sensor readings | 6859 |
| commands.txt | Load commands, QA run, then summary and alert commands per day | 10 |

Volumes in this sample are reduced for email delivery; the hidden evaluation set is larger and uses the same schema. (Here 3 days; the evaluation set covers 7 days, about 16,000 readings.)

## Column reference
Conventions: dates `YYYY-MM-DD`; timestamps `YYYY-MM-DD HH:MM:SS` (24h, IST, no timezone suffix); money in Rs as plain decimals (no commas, no symbol); percentages as plain numbers (12.5 = 12.5%); booleans `true`/`false`; IDs uppercase with a fixed prefix.

### stations.csv
| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| station_id | string | AWS-nn | AWS-01 … AWS-08 | Primary key |
| station_name | string | - | free text |  |
| district | string | - | Dakshina Kannada, Udupi, Kodagu | District alert = highest station level |
| latitude | decimal | degrees, 5 dp |  | Not used by any rule |
| longitude | decimal | degrees, 5 dp |  | Not used by any rule |
| sensors | string | semicolon-separated | TEMP;HUMIDITY;RAIN | All stations carry all three |

### sensor_ranges.csv
| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| sensor | string | - | TEMP, HUMIDITY, RAIN | Primary key |
| unit | string | - | degC, pct, mm_per_15min |  |
| min_value | decimal | unit of the sensor |  | Inclusive |
| max_value | decimal | unit of the sensor |  | Inclusive |

### readings.csv
| Column | Type | Units / format | Allowed values | Notes |
|---|---|---|---|---|
| station_id | string | AWS-nn | must exist in stations.csv |  |
| timestamp | timestamp | YYYY-MM-DD HH:MM:SS | minutes 00, 15, 30, 45 | Sorted by timestamp, station, sensor; re-sent duplicates appear one slot later |
| sensor | string | - | TEMP, HUMIDITY, RAIN |  |
| value | decimal | 1 dp, unit from sensor_ranges.csv |  | RAIN is mm fallen in that 15-minute slot |

## Command file format
`commands.txt` holds one command per line as `COMMAND_NAME|arg1|arg2|...`. Commands must be processed in file order, top to bottom. Lines starting with `#` are comments and blank lines are ignored.

| Command | Arguments (in order) | Meaning |
|---|---|---|
| LOAD_STATIONS | file | Load stations.csv |
| LOAD_RANGES | file | Load sensor_ranges.csv |
| LOAD_READINGS | file | Load readings.csv |
| RUN_QA | (none) | Apply range, duplicate, spike and interpolation rules; print the QA log |
| DAILY_SUMMARY | YYYY-MM-DD | Print the summary of every station for that day |
| DISTRICT_ALERTS | YYYY-MM-DD | Print the alert level of every district for that day |

`flag` is one of RANGE, DUPLICATE, SPIKE, FILLED. `raw_value` is `NONE` for a slot that had no row and was filled; `value_used` is `NONE` for a rejected reading that was not filled. `status` is VALID or INVALID; on INVALID rows every value column and `alert_level` is `NONE` (the missing_* counts are still given). `alert_level` is NONE, HEAVY, VERY_HEAVY or EXTREMELY_HEAVY. missing_* counts are after filling. In district_alerts.csv, `max_station_id`/`max_rainfall_mm` are `NONE` when no valid station of the district has an alert; ties go to the lower station_id.

## Planted scenarios
Line numbers count the header row as line 1, so the first data row of a CSV is line 2. For commands.txt the line number is the physical line in the file (comment lines included).

- **Gap of exactly 4 missing readings versus 5** — AWS-07: the logger sends nothing from 2026-10-05 12:00:00 to 2026-10-05 12:45:00 (4 slots, all three sensors). TEMP/HUMIDITY are filled linearly between readings.csv line 1148 (AWS-07 TEMP 2026-10-05 11:45:00, value 22.1) and readings.csv line 1256 (AWS-07 TEMP 2026-10-05 13:00:00, value 23.0) and flagged FILLED; the 4 RAIN slots stay missing (rainfall is never interpolated). Compare AWS-01: TEMP is absent for 5 slots from 2026-10-06 15:30:00 to 2026-10-06 16:30:00 (between readings.csv line 3740 (AWS-01 TEMP 2026-10-06 15:15:00, value 30.2) and readings.csv line 3879 (AWS-01 TEMP 2026-10-06 16:45:00, value 29.8)) — too long, stays missing.
- **Spike at the very first reading of the day (no previous value, accepted)** — readings.csv line 4578 (AWS-02 TEMP 2026-10-07 00:00:00, value 30.7) is the first TEMP reading of its day and is 7.2 degC above the previous day's last reading readings.csv line 4554 (AWS-02 TEMP 2026-10-06 23:45:00, value 23.5); the next reading is not within 2 degC of it. It has no previous value on its own day, so it is ACCEPTED (it should appear as that day's TEMP max).
- **Station-day with exactly 20% missing (valid)** — 20% of 96 is 19.2, so a whole number of readings can never be exactly 20%. The boundary pair: AWS-01 on 2026-10-07 is missing 19 TEMP readings from 2026-10-07 03:00:00 (19.79% → VALID, the gap is too long to fill); AWS-04 on 2026-10-06 is missing 20 TEMP readings from 2026-10-06 03:00:00 (20.83% → INVALID, no summary).
- **Rainfall total of exactly 64.5 mm (not HEAVY)** — AWS-03 on 2026-10-06 totals exactly 64.5 mm of accepted rain → no alert for that station. AWS-02 on 2026-10-06 (same district, same day) totals 81.3 mm → HEAVY, so the district alert is HEAVY.
- **Humidity reading of 100.0 (valid) and 100.1 (rejected)** — During the very heavy rain at AWS-06: readings.csv line 2828 (AWS-06 HUMIDITY 2026-10-06 05:30:00, value 100.0) humidity 100.0 is valid; readings.csv line 3059 (AWS-06 HUMIDITY 2026-10-06 08:00:00, value 100.1) humidity 100.1 is out of range → rejected and then filled as a 1-reading gap.

Extra traps (realistic things your validation should catch):

- **Rainfall exactly on the VERY_HEAVY threshold** — AWS-08 on 2026-10-06 totals exactly 115.5 mm → HEAVY (not VERY_HEAVY). AWS-06 on 2026-10-06 totals 131.7 mm → VERY_HEAVY; AWS-04 on 2026-10-05 totals 207.1 mm → EXTREMELY_HEAVY.
- **Out-of-range values** — readings.csv line 5745 (AWS-05 TEMP 2026-10-07 12:15:00, value 85.3) TEMP 85.3 → rejected (then filled from its neighbours); readings.csv line 6275 (AWS-05 RAIN 2026-10-07 17:45:00, value 112.0) RAIN 112.0 mm in 15 min → rejected, not counted in the rainfall total and not filled.
- **True spike vs confirmed step change** — readings.csv line 1208 (AWS-05 TEMP 2026-10-05 12:30:00, value 36.2) jumps 6.8 degC and the next reading drops back → SPIKE, rejected (then filled). readings.csv line 1731 (AWS-05 TEMP 2026-10-05 18:00:00, value 23.9) drops 6.1 degC but readings.csv line 1755 (AWS-05 TEMP 2026-10-05 18:15:00, value 24.1) stays within 2 degC of it → accepted (a real squall). The spike check always compares with the last ACCEPTED value.
- **Change of exactly 5.0 degC** — readings.csv line 1235 (AWS-08 TEMP 2026-10-05 12:45:00, value 30.6) is exactly 5.0 above readings.csv line 1214 (AWS-08 TEMP 2026-10-05 12:30:00, value 25.6) → not more than 5, so accepted. Compare in tenths (integers) — 31.3 - 26.3 in floating point is 5.000000000000002.
- **Duplicate readings** — readings.csv line 1430 (AWS-06 TEMP 2026-10-05 14:30:00, value 29.4) repeats readings.csv line 1397 (AWS-06 TEMP 2026-10-05 14:30:00, value 29.0) with a different value; readings.csv line 3283 (AWS-07 HUMIDITY 2026-10-06 10:00:00, value 77.6) and readings.csv line 5636 (AWS-07 RAIN 2026-10-07 10:45:00, value 0.0) repeat their originals exactly. Keep the first in file order, reject the second with flag DUPLICATE.

## What is NOT in this pack
Expected outputs are not provided for this set. Validate your engine with your own test suite against the rules in your brief (BR-01 … BR-07). A separate hidden input set with the same schema will be used at final evaluation; outputs are compared field-for-field, so follow the column formats above exactly in your own output.

## Output format expected at evaluation
Produce these files (CSV, header row, same conventions as above). Column order matters.

### qa_log.csv
One row per rejected or filled reading, ordered by station_id, sensor (TEMP, HUMIDITY, RAIN), timestamp, then file order.

Columns in order: `station_id`, `sensor`, `timestamp`, `raw_value`, `flag`, `value_used`

### daily_summary.csv
One row per station per day, ordered by date then station_id.

Columns in order: `date`, `station_id`, `district`, `status`, `temp_min`, `temp_max`, `temp_mean`, `humidity_min`, `humidity_max`, `humidity_mean`, `rainfall_mm`, `missing_temp`, `missing_humidity`, `missing_rain`, `alert_level`

### district_alerts.csv
One row per district per day, ordered by date then district.

Columns in order: `date`, `district`, `alert_level`, `max_station_id`, `max_rainfall_mm`
