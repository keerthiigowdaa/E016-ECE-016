import sys
sys.path.insert(0, "src")

from interpolation import interpolate_missing


def test_interpolation():

    readings = [
        {
            "station_id": "ST001",
            "timestamp": "2026-11-10 09:00",
            "sensor": "temperature",
            "value": 20
        },
        {
            "station_id": "ST001",
            "timestamp": "2026-11-10 09:30",
            "sensor": "temperature",
            "value": 26
        }
    ]

    result = interpolate_missing(readings)

    assert len(result) == 3
    assert result[2]["value"] == 23

    print("Interpolation test passed!")


if __name__ == "__main__":
    test_interpolation()