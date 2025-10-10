from flask import Blueprint, jsonify, request, current_app
from app.services import cosine_similarity, tokenizer
from werkzeug.exceptions import BadRequest
from concurrent.futures import ThreadPoolExecutor


estimation_blueprint = Blueprint('estimation', __name__, url_prefix="/api/v1")
executor = ThreadPoolExecutor()


@estimation_blueprint.route('/estimate', methods=['POST'])
def estimate_similarity():
    data = request.get_json()

    if not data:
        current_app.logger.warning("No data provided for similarity estimation")
        raise BadRequest("No data provided")
    try:
        user_prompt = data['user_prompt']
        augmented_prompt = data['augmented_prompt']
        generated_text = data['generated_text']
    except KeyError as e:
        current_app.logger.warning("Empty %s provided", e)
        raise BadRequest("Both %s must be provided and non-empty" % e)

    executor.submit(cosine_similarity.calculate_cosine_similarity(augmented_prompt, generated_text))
    executor.submit(tokenizer.get_tokens(generated_text, current_app.config['YC_FOLDER_ID'], current_app.config['MODEL_NAME']))
    return jsonify({'status': 'ok'})
    # try:
    #     similarity_score = cosine_similarity.calculate_cosine_similarity(augmented_prompt, generated_text)
    #     estimation_result = {
    #         'cosine_similarity_score': round(similarity_score, 3)
    #     }
    #     current_app.logger.info("Successfully calculated cosine similarity: %s", estimation_result['cosine_similarity_score'])
    #     return jsonify(estimation_result), 200
    # except Exception as e:
    #     current_app.logger.error("Error calculating cosine similarity: %s", str(e))
    #     raise
