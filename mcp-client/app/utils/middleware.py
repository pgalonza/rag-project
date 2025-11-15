import uuid
from flask import g, request, Flask, Response
from typing import Dict


def add_middleware(app: Flask) -> None:
    @app.before_request
    def before_request() -> None:
        request_id: str = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        g.request_id = request_id

    # Add security headers middleware
    @app.after_request
    def after_request(response: Response) -> Response:
        # Add security headers
        security_headers: Dict[str, str] = app.config.get('SECURITY_HEADERS', {})
        for header, value in security_headers.items():
            response.headers[header] = value
        return response
