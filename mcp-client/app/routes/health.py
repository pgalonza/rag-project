from flask import Blueprint, jsonify

health_blueprint = Blueprint('health', __name__)

@health_blueprint.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint.
    ---
    responses:
      200:
        description: Service is healthy
    """
    return jsonify({
        'status': 'healthy',
        'service': 'augmented-generation-api'
    }), 200
