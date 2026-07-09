from src.main import greet

def test_greet_returns_expected_string():
    assert greet("Tester") == "Hello, Tester!"
