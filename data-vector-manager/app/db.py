from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from flask import current_app, g


def init_app(app):
    app.teardown_appcontext(close_db)

def create_all():
    db = get_db()
    if not db.collection_exists(current_app.config['COLLECTION_NAME']):
        db.create_collection(
            collection_name=current_app.config['COLLECTION_NAME'],
            vectors_config=VectorParams(size=768, distance=Distance.COSINE),
        )

def get_db():
    if 'db' not in g:
        g.db = QdrantClient(url=current_app.config['QDRANT_URL'])
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def add_documents(documents):
    db = get_db()
    embeddings = YandexGPTEmbeddings()
    vector_store = QdrantVectorStore(
        client=db,
        collection_name=current_app.config['COLLECTION_NAME'],
        embedding=embeddings,
    )
    result = vector_store.add_documents(documents=documents)
    return result

def get_documents(ids):
    db = get_db()

    embeddings = YandexGPTEmbeddings()
    vector_store = QdrantVectorStore(
        client=db,
        collection_name=current_app.config['COLLECTION_NAME'],
        embedding=embeddings,
    )

    documents = vector_store.get_by_ids(ids)

    return documents

def search_documents(query, number):
    db = get_db()

    embeddings = YandexGPTEmbeddings()
    vector_store = QdrantVectorStore(
        client=db,
        collection_name=current_app.config['COLLECTION_NAME'],
        embedding=embeddings,
    )

    documents = vector_store.similarity_search(query, number)

    return documents