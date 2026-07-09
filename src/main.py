from flask import Flask, jsonify, render_template_string
from flasgger import Swagger

app = Flask(__name__)


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
        "title": "Greeting API",
        "description": "A simple Flask API with Swagger UI",
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


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True)
