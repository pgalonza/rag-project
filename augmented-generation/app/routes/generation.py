import requests
from flask import Blueprint, jsonify, request, current_app, g
from app.services import generation_service
from app.utils import validators

generation_blueprint = Blueprint('generation', __name__, url_prefix="/api/v1")

@generation_blueprint.route('/generation', methods=['GET'])
def augmented_generation():
    user_prompt = request.args.get('prompt')
    # Sanitize input
    user_prompt = validators.sanitize_input(user_prompt)

    # Validate prompt
    is_valid, message = validators.validate_prompt(user_prompt)
    if not is_valid:
        current_app.logger.warning('Invalid prompt: %s', message)
        raise ValueError(message)

    current_app.logger.info('User prompt: %s', user_prompt)

    documents = requests.get(
        current_app.config['DOCUMENTS_SEARCH_URL'],
        params={'query': user_prompt, 'number': 1},
        timeout=5,
        headers={'X-Request-ID': g.request_id}
    )
    current_app.logger.info('Get document status: %s', documents.status_code)

    if documents.status_code != 200:
        current_app.logger.error('Documents service error: %s', documents.status_code)
        raise requests.exceptions.RequestException('Failed to retrieve documents')

    documents_data = documents.json()
    if not documents_data or len(documents_data) == 0:
        current_app.logger.warning('No documents found for query')
        raise ValueError('No relevant documents found')

    context = documents_data[0]['content']
    current_app.logger.info('Document from DB: %s', context)

    prompt = generation_service.create_message(user_prompt, current_app.config['ASSISTENT_ROLE'], context)
    response = generation_service.send_message(
        prompt,
        current_app.config['YC_FOLDER_ID'],
        current_app.config['MODEL_NAME'],
        current_app.config['MODEL_TEMPERATURE'])
    result = response.alternatives[0].text
    requests.post(
        current_app.config['LLM_ESTIMATION_URL'],
        json={'user_prompt': user_prompt, 'augmented_prompt': context, 'generated_text': result},
        timeout=5,
        headers={'X-Request-ID': g.request_id}
    )
    headers = {
        'Request-ID': g.request_id,
        'Content-Type': 'application/json'
    }
    return jsonify({'text': result}), 200, headers
