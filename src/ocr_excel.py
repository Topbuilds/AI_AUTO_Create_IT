from pathlib import Path
import platform

from PIL import Image
import pytesseract
from openpyxl import Workbook


def configure_tesseract_path() -> None:
    if platform.system() != "Windows":
        return

    default_path = Path("C:/Program Files/Tesseract-OCR/tesseract.exe")
    if default_path.exists():
        pytesseract.pytesseract.tesseract_cmd = str(default_path)


configure_tesseract_path()


def ocr_image_to_text(image_path: Path | str) -> str:
    """Perform OCR on the image and return the extracted text."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    with Image.open(path) as image:
        text = pytesseract.image_to_string(image, lang="chi_sim+eng")

    return text.strip()


def text_to_excel(text: str, excel_path: Path | str) -> Path:
    """Write OCR text to an Excel workbook, one line per row."""
    path = Path(excel_path)
    workbook = Workbook()
    sheet = workbook.active

    for row_index, line in enumerate(text.splitlines(), start=1):
        sheet.cell(row=row_index, column=1, value=line)

    workbook.save(path)
    return path


def ocr_image_to_excel(image_path: Path | str, excel_path: Path | str | None = None) -> Path:
    """Run OCR on the input image and export the result to an Excel file."""
    image_path = Path(image_path)
    if excel_path is None:
        excel_path = image_path.with_suffix(".xlsx")

    text = ocr_image_to_text(image_path)
    return text_to_excel(text, excel_path)
