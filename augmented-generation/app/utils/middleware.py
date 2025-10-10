import uuid
from flask import g, request

def add_middleware(app):
    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-ID')
        if not request_id:
            request_id = str(uuid.uuid4())
        g.request_id = request_id

    # Add security headers middleware
    @app.after_request
    def after_request(response):
        # Add security headers
        security_headers = app.config.get('SECURITY_HEADERS', {})
        for header, value in security_headers.items():
            response.headers[header] = value
        return response