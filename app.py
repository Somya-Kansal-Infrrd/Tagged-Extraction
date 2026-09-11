"""Flask application for tagged extraction."""

from flask import Flask

from controllers.extraction_controller import tagged_extraction


app = Flask(__name__)


app.add_url_rule(
    "/api/tagged-extraction",
    view_func=tagged_extraction,
    methods=["POST"],
)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
    )