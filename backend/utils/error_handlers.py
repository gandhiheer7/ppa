from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = {
            "error": e.name,
            "message": e.description,
            "status_code": e.code
        }
        return jsonify(response), e.code

    @app.errorhandler(Exception)
    def handle_general_exception(e):
        response = {
            "error": "Internal Server Error",
            "message": "An unexpected error occurred.",
            "status_code": 500
        }
        return jsonify(response), 500
