from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings.yandex import YandexGPTEmbeddings
from flask import current_app, g

_vector_store = None

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
        g.db = QdrantClient(
            url=current_app.config['QDRANT_URL'],
            timeout=30,
        )
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def get_vector_store():
    global _vector_store
    if _vector_store is None:
        db = get_db()
        embeddings = YandexGPTEmbeddings()
        _vector_store = QdrantVectorStore(
            client=db,
            collection_name=current_app.config['COLLECTION_NAME'],
            embedding=embeddings,
        )
    return _vector_store

def add_documents(documents):
    vector_store = get_vector_store()
    return vector_store.add_documents(documents=documents)

def get_documents(ids):
    vector_store = get_vector_store()
    return vector_store.get_by_ids(ids)

def search_documents(query, number):
    vector_store = get_vector_store()
    return vector_store.similarity_search(query, number)
