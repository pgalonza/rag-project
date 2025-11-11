from flask import Blueprint, render_template, request, jsonify
from app.utils import mcp_client


chat_blueprint = Blueprint('chat', __name__, url_prefix="/")
api_blueprint = Blueprint('api', __name__, url_prefix="/api/v1")
@chat_blueprint.route('/')
async def index():
    return render_template('index.html')

@chat_blueprint.route('/chat', methods=['POST'])
async def chat():
    data = request.get_json()
    message = data.get('message', '')

    if not message:
        return jsonify({'response': 'Empty message'}), 400

    try:
        # Use YandexGPT if configured, otherwise fall back to MCP client
        response = await mcp_client.send_message({"messages": [{"role": "user", "content": message}]})
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'response': f'Error: {str(e)}'}), 500

# @api_blueprint.route('/tools', methods=['GET'])
# def list_tools():
#     try:
#         tools = asyncio.run(get_tools())
#         return jsonify({'tools': tools})
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
