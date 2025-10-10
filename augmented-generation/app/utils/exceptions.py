import requests
from flask import jsonify

class ValidationError(Exception):
    """Exception raised for validation errors."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ServiceError(Exception):
    """Exception raised for service errors."""
    def __init__(self, message, status_code=502):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class TimeoutError(Exception):
    """Exception raised for timeout errors."""
    def __init__(self, message="Service timeout"):
        super().__init__(message)
        self.message = message
        self.status_code = 504

def register_error_handlers(app):
    # Register error handlers
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error('Internal error: %s', str(error))
        return jsonify({'error': 'Internal server error'}), 500

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        app.logger.warning('Validation error: %s', str(error))
        return jsonify({'error': str(error)}), 400

    @app.errorhandler(requests.exceptions.Timeout)
    def handle_timeout(error):
        app.logger.error('Service timeout: %s', str(error))
        return jsonify({'error': 'Service timeout'}), 504

    @app.errorhandler(requests.exceptions.RequestException)
    def handle_request_exception(error):
        app.logger.error('Service error: %s', str(error))
        return jsonify({'error': 'Service error'}), 502

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        app.logger.error('Unexpected error: %s', str(error))
        return jsonify({'error': 'Internal server error'}), 500