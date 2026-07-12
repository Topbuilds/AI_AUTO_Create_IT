from src.main import app, greet
from src.ocr_excel import text_to_word


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


def test_home_page_is_available():
    client = app.test_client()

    response = client.get("/")
    assert response.status_code == 200
    assert b"OCR Transfer" in response.data


def test_text_to_word_creates_docx(tmp_path):
    output_path = tmp_path / "ocr.docx"

    result = text_to_word("Hello OCR\nWorld", output_path)

    assert result == output_path
    assert output_path.exists()

    from docx import Document

    document = Document(output_path)
    text = "\n".join(paragraph.text for paragraph in document.paragraphs)
    assert "Hello OCR" in text
    assert "World" in text
