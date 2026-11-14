# E016 - Weather Station Data QA

## Project Details
Team ID: E016
Team Members: Keerthi V and Khushi R
Programming Language: Python 3.10+
IDE: Visual Studio Code

## Business Rules

BR-01: Register weather stations with station ID, district and sensors.

BR-02: Accept readings at 15-minute intervals.

BR-03: Temperature must be between -10 and 50 degrees Celsius.

BR-04: Humidity must be between 0 and 100 percent.

BR-05: Rainfall must be between 0 and 100 mm per 15 minutes.

BR-06: Detect temperature spikes.

BR-07: Identify missing readings.

BR-08: Fill gaps of up to four consecutive readings using linear interpolation.

BR-09: Never interpolate rainfall.

BR-10: Mark station-days with more than 20% missing readings as INVALID.

BR-11: Calculate daily minimum, maximum and mean temperature.

BR-12: Calculate daily minimum, maximum and mean humidity.
BR-13: Calculate total accepted rainfall.

BR-14: Generate rainfall alerts.

BR-15: Detect duplicate readings and reject the second reading.

BR-16: Generate QA logs and daily reports.