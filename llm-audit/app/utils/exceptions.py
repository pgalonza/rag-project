from flask import jsonify

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

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        app.logger.error('Unexpected error: %s', str(error))
        return jsonify({'error': 'Internal server error'}), 500
