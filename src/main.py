import os
from pathlib import Path

from flask import Flask, jsonify, render_template, render_template_string, request, send_from_directory
from flasgger import Swagger
from werkzeug.utils import secure_filename

try:
    from .ocr_excel import ocr_image_to_excel, ocr_image_to_word
except ImportError:  # pragma: no cover - supports running as a script
    from ocr_excel import ocr_image_to_excel, ocr_image_to_word

app = Flask(__name__)
UPLOAD_FOLDER = (Path(__file__).resolve().parent.parent / "uploads").resolve()
UPLOAD_FOLDER.mkdir(exist_ok=True)
app.config["UPLOAD_FOLDER"] = str(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "bmp", "tiff", "gif"}


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.get("/apidocs/")
def swagger_ui():
    return render_template_string(
        """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Swagger UI</title>
            <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css" />
        </head>
        <body>
            <div id="swagger-ui"></div>
            <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
            <script>
                window.onload = () => {
                    SwaggerUIBundle({
                        url: "/apispec_1.json",
                        dom_id: "#swagger-ui"
                    });
                };
            </script>
        </body>
        </html>
        """
    )


swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "OCR Export API",
        "description": "Upload images to extract text and export the results as Excel or Word files",
        "version": "1.0.0"
    }
})


def greet(name: str) -> str:
    return f"Hello, {name}!"


@app.get("/greet/<name>")
def greet_route(name: str):
    """
    Return a greeting message.
    ---
    parameters:
      - name: name
        in: path
        type: string
        required: true
        description: Name to greet
    responses:
      200:
        description: Greeting generated successfully
        schema:
          type: object
          properties:
            message:
              type: string
    """
    return jsonify({"message": greet(name)})


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/ocr-to-excel")
def ocr_to_excel_route():
    """
    Upload an image and return a download link for the exported Excel file.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Image file to OCR
    responses:
      200:
        description: Excel file generated successfully
        schema:
          type: object
          properties:
            filename:
              type: string
            download_url:
              type: string
      400:
        description: Invalid file or request
    """
    if "file" not in request.files:
        return jsonify({"error": "Missing file field."}), 400

    file = request.files["file"]
    filename = file.filename
    if not filename:
        return jsonify({"error": "No selected file."}), 400

    if not allowed_file(filename):
        return jsonify({"error": "Unsupported file type."}), 400

    safe_name = secure_filename(filename)
    input_path = Path(app.config["UPLOAD_FOLDER"]) / safe_name
    file.save(input_path)

    output_path = input_path.with_suffix(".xlsx")
    ocr_image_to_excel(input_path, output_path)

    return jsonify({
        "filename": output_path.name,
        "download_url": f"/download/{output_path.name}"
    })


@app.post("/ocr-to-word")
def ocr_to_word_route():
    """
    Upload an image and return a download link for the exported Word file.
    ---
    consumes:
      - multipart/form-data
    parameters:
      - name: file
        in: formData
        type: file
        required: true
        description: Image file to OCR
    responses:
      200:
        description: Word file generated successfully
        schema:
          type: object
          properties:
            filename:
              type: string
            download_url:
              type: string
      400:
        description: Invalid file or request
    """
    if "file" not in request.files:
        return jsonify({"error": "Missing file field."}), 400

    file = request.files["file"]
    filename = file.filename
    if not filename:
        return jsonify({"error": "No selected file."}), 400

    if not allowed_file(filename):
        return jsonify({"error": "Unsupported file type."}), 400

    safe_name = secure_filename(filename)
    input_path = Path(app.config["UPLOAD_FOLDER"]) / safe_name
    file.save(input_path)

    output_path = input_path.with_suffix(".docx")
    ocr_image_to_word(input_path, output_path)

    return jsonify({
        "filename": output_path.name,
        "download_url": f"/download/{output_path.name}"
    })


@app.get("/download/<path:filename>")
def download_excel(filename: str):
    """
    Download the generated Excel or Word file.
    ---
    parameters:
      - name: filename
        in: path
        type: string
        required: true
        description: Generated Excel or Word filename to download
    responses:
      200:
        description: File downloaded successfully
    """
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Run the Flask API server or OCR an image to Excel or Word.")
    parser.add_argument(
        "--ocr",
        dest="image_path",
        help="Path to the input image file to OCR and export.",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path. Defaults to the image path with .xlsx or .docx extension depending on the selected format.",
    )
    parser.add_argument(
        "--word",
        action="store_true",
        help="Export OCR output as a Word document instead of Excel.",
    )

    args = parser.parse_args()
    if args.image_path:
        if args.word:
            from ocr_excel import ocr_image_to_word

            image_file = Path(args.image_path)
            output_file = Path(args.output) if args.output else image_file.with_suffix(".docx")
            word_path = ocr_image_to_word(image_file, output_file)
            print(f"Saved OCR Word file at: {word_path}")
        else:
            from ocr_excel import ocr_image_to_excel

            image_file = Path(args.image_path)
            output_file = Path(args.output) if args.output else image_file.with_suffix(".xlsx")
            excel_path = ocr_image_to_excel(image_file, output_file)
            print(f"Saved OCR Excel file at: {excel_path}")
        return

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)


if __name__ == "__main__":
    main()
