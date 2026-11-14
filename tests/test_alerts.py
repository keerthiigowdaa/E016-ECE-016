import sys
sys.path.insert(0, "src")

from alerts import get_rainfall_alert, generate_district_alerts


def test_alerts():

    assert get_rainfall_alert(64.5) == "NO_ALERT"
    assert get_rainfall_alert(70) == "HEAVY"
    assert get_rainfall_alert(120) == "VERY_HEAVY"
    assert get_rainfall_alert(210) == "EXTREMELY_HEAVY"

    summaries = [
        {"district": "Bengaluru", "rainfall_total": 70},
        {"district": "Bengaluru", "rainfall_total": 120},
        {"district": "Mysuru", "rainfall_total": 50}
    ]

    result = generate_district_alerts(summaries)

    assert result["Bengaluru"] == "VERY_HEAVY"
    assert result["Mysuru"] == "NO_ALERT"

    print("All rainfall alert tests passed!")


if __name__ == "__main__":
    test_alerts()