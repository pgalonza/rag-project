from flask import Blueprint, jsonify, request, current_app
from app.services import data_service
from app import db
from werkzeug.exceptions import BadRequest

document_blueprints = Blueprint('documents', __name__, url_prefix="/api/v1")

@document_blueprints.route('/documents', methods=['POST'])
def create_document():
    """
    Create a new document.
    ---
    parameters:
      - in: body
        name: document
        schema:
          id: Document
          type: array
          required:
            - content
          items:
            type: object
            properties:
              content:
                type: string
                description: The content of the document.
                example: This is the content of the document.
              metadata:
                type: object
                description: Metadata for the document.
                properties:
                  key:
                    type: string
                    description: The key of the metadata.
                  value:
                    type: string
                    description: The value of the metadata.
    responses:
      201:
        description: Document created successfully.
      400:
        description: Bad request.
    """

    current_app.logger.info("Creating new document(s)")
    data = request.get_json()

    if not data:
        current_app.logger.warning("No data provided for document creation")
        raise BadRequest("No data provided")

    prepared_documents = data_service.prepare_documents(data)
    result = db.add_documents(prepared_documents)

    current_app.logger.info("Successfully created %d document(s)", len(result) if isinstance(result, list) else 1)
    return jsonify(result), 201


@document_blueprints.route('/documents', methods=['GET'])
def get_documents():
    """
    Get documents by ID.
    ---
    parameters:
      - in: query
        name: ids
        type: string
        required: true
        description: Comma-separated list of document IDs.
    responses:
      200:
        description: Documents fetched successfully.
      400:
        description: Bad request.
    """

    ids = request.args.get('ids')
    current_app.logger.info("Fetching documents with ids: %s", ids)

    if not ids:
        current_app.logger.warning("No document IDs provided")
        raise BadRequest("No document IDs provided")

    document_ids = [id.strip() for id in ids.split(',')]
    documents = db.get_documents(document_ids)

    result = []
    for document in documents:
        result.append(
            {
                "content": document.page_content,
                "metadata": document.metadata
            }
        )

    current_app.logger.info("Successfully fetched %d document(s)", len(result))
    return jsonify(result), 200


@document_blueprints.route('/documents/search', methods=['GET'])
def search_documents():
    """
    Search documents by query.
    ---
    parameters:
      - in: query
        name: query
        type: string
        required: true
        description: The query to search for.
      - in: query
        name: number
        type: integer
        default: 4
        description: The number of documents to return.
    responses:
      200:
        description: Documents fetched successfully.
      400:
        description: Bad request.
    """

    query = request.args.get('query')
    number_of_docs = request.args.get('number', 4)

    current_app.logger.info("Searching documents with query: %s, number: %s", query, number_of_docs)

    if not query:
        current_app.logger.warning("No query provided for document search")
        raise BadRequest("No query provided")

    # Convert number_of_docs to int with error handling
    try:
        number_of_docs = int(number_of_docs)
    except (ValueError, TypeError):
        current_app.logger.warning("Invalid number parameter, using default value of 4")
        number_of_docs = 4

    documents = db.search_documents(query, number_of_docs)

    result = []
    for document in documents:
        result.append(
            {
                "content": document.page_content,
                "metadata": document.metadata
            }
        )

    current_app.logger.info("Successfully found %d document(s) for query: %s", len(result), query)
    return jsonify(result), 200