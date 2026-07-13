from PIL import Image

from src.main import app, greet
from src.ocr_excel import ocr_image_to_text, text_to_word
from src.database import init_db, list_submission_records, save_submission_record


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


def test_admin_reviews_page_is_available():
    client = app.test_client()

    response = client.get("/admin/reviews")
    assert response.status_code == 200
    assert b"Admin Review" in response.data


def test_database_can_store_submission_record(tmp_path):
    db_path = tmp_path / "review.db"
    init_db(f"sqlite:///{db_path}")

    record = save_submission_record(
        db_url=f"sqlite:///{db_path}",
        original_filename="sample.png",
        original_path=str(tmp_path / "sample.png"),
        output_filename="sample.xlsx",
        output_path=str(tmp_path / "sample.xlsx"),
        output_format="excel",
    )

    records = list_submission_records(f"sqlite:///{db_path}")
    assert record.id is not None
    assert len(records) == 1
    assert records[0].original_filename == "sample.png"


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


def test_ocr_image_to_text_prefers_paddleocr(monkeypatch, tmp_path):
    image_path = tmp_path / "sample.png"
    Image.new("RGB", (1, 1), color="white").save(image_path)

    monkeypatch.setattr("src.ocr_excel._run_paddleocr", lambda image_path: "hello from paddle", raising=False)
    monkeypatch.setattr("src.ocr_excel.pytesseract.image_to_string", lambda image, lang=None: "hello from tesseract")

    assert ocr_image_to_text(image_path) == "hello from paddle"
