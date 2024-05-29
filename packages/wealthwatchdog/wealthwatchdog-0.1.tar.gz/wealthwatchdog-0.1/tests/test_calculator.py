from WealthWatchDog import calculator


def test_calculate_savings():
    assert calculator.calculate_savings(10000, 3000, 2000) == 34000
