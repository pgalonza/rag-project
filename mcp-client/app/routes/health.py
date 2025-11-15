from flask import Blueprint, jsonify, Response
from typing import Any, Dict, Tuple

health_blueprint: Blueprint = Blueprint('health', __name__)

@health_blueprint.route('/health', methods=['GET'])
def health_check() -> Tuple[Response, int]:
    """
    Health check endpoint.
    ---
    responses:
      200:
        description: Service is healthy
    """
    response_data: Dict[str, str] = {
        'status': 'healthy',
        'service': 'augmented-generation-api'
    }
    return jsonify(response_data), 200
