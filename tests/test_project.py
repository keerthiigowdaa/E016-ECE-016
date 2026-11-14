import sys
sys.path.insert(0, "src")

from alerts import get_rainfall_alert


def test_rainfall_alerts():

    assert get_rainfall_alert(50) == "NO_ALERT"
    assert get_rainfall_alert(64.5) == "NO_ALERT"
    assert get_rainfall_alert(64.6) == "HEAVY"
    assert get_rainfall_alert(115.5) == "HEAVY"
    assert get_rainfall_alert(115.6) == "VERY_HEAVY"
    assert get_rainfall_alert(204.4) == "VERY_HEAVY"
    assert get_rainfall_alert(204.5) == "EXTREMELY_HEAVY"

    print("All rainfall alert tests passed!")


if __name__ == "__main__":
    test_rainfall_alerts()