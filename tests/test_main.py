from src.main import app, greet


def test_greet_returns_expected_string():
    assert greet("Tester") == "Hello, Tester!"


def test_swagger_docs_are_available():
    client = app.test_client()

    docs_response = client.get("/apidocs/")
    assert docs_response.status_code == 200
    assert b"Swagger UI" in docs_response.data


def test_greeting_endpoint_returns_json():
    client = app.test_client()

    response = client.get("/greet/Tester")
    assert response.status_code == 200
    assert response.get_json() == {"message": "Hello, Tester!"}
